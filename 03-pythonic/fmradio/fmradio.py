import asyncio
import re
import signal
from pathlib import Path
from typing import Literal, Optional, Union

import click
import numpy as np
import sounddevice as sd
import soundfile as sf
import uvloop
from scipy.signal import decimate, lfilter, remez

Hertz = int


class Sample:
    """
    Cette classe embarque les opérations à appliquer sur un tableau NumPy
    d'échantillons I/Q.
    """

    array: np.ndarray

    mono_signal: Hertz = 15_000
    fm_bandwidth: Hertz = 220_500

    def __init__(self, array: np.ndarray):
        self.array = array

    def offset(self, freq_offset: Hertz, freq_sr: Hertz) -> "Sample":
        "Décalage de fréquence."
        t = np.arange(self.array.size) / freq_sr
        return Sample(
            self.array * np.exp(-1.0j * 2.0 * np.pi * freq_offset * t)
        )

    def downsample(self, facteur) -> "Sample":
        "Sous-échantillonage."
        res = decimate(self.array, facteur)
        return Sample(res)

    def extraction(self) -> "Sample":
        return Sample(np.angle(self.array[1:] * np.conj(self.array[:-1])))

    def lowpass(self) -> "Sample":
        "FIR passe-bas pour le signal mono."
        coefficients = remez(
            256,
            [
                0,
                self.mono_signal,
                self.mono_signal + 4000,
                self.fm_bandwidth / 2,
            ],
            [1, 0],
            Hz=self.fm_bandwidth,
        )
        return Sample(lfilter(coefficients, 1.0, self.array))

    def deemphasis(self) -> "Sample":
        """De-emphasis filter.

        Ce filtre est spécifié à partir d'un temps caractéristique
        (50 µs en Europe, 75 µs aux États-Unis) où le filtre atténue 3dB.
        """
        d = self.fm_bandwidth * 50e-6
        decay = np.exp(-1 / d)
        b = [1 - decay]
        a = [1, -decay]
        return Sample(lfilter(b, a, self.array))

    def audio_mono(self, sampling_rate, offset) -> np.ndarray:
        "Décodage de la piste audio mono."
        return (
            self.offset(offset, sampling_rate)
            .downsample(int(sampling_rate // Sample.fm_bandwidth))
            .extraction()
            .lowpass()
            .deemphasis()
            .downsample(int(Sample.fm_bandwidth // 44100))
            .array
        )


interrupt = False


async def file_streaming(
    audioqueue: asyncio.Queue[np.ndarray],
    file: Path,
    blocksize: int,
    offset: Hertz = 200_000,
    sampling_rate: Hertz = 1_102_500,
):
    "Décodage depuis un fichier binaire produit par rtl_sdr."

    global interrupt

    with file.open("rb") as fh:
        while not interrupt:
            buffer = fh.read(2 * blocksize)
            if len(buffer) < 2 * blocksize:
                interrupt = True

            iqdata = np.frombuffer(buffer, dtype=np.uint8)
            iqdata = (2 * iqdata - 255) / 256.0
            samples = iqdata.view(complex)

            while audioqueue.qsize() > 10:
                # inutile de trop remplir la file, on peut attendre...
                await asyncio.sleep(0.1)

            await audioqueue.put(
                Sample(samples).audio_mono(sampling_rate, offset)
            )

    # On remet le flag à False pour pouvoir interrompre l'écoute
    # même si la lecture est terminée
    interrupt = False


async def sdr_streaming(
    audioqueue: asyncio.Queue[np.ndarray],
    center_frequency: Hertz,
    blocksize: int,
    offset: Hertz = 200_000,
    sampling_rate: Hertz = 1_102_500,
    gain: Union[int, Literal["auto"]] = "auto",
):
    "Décodage en temps réel depuis une antenne."
    from rtlsdr import RtlSdr

    sdr = RtlSdr()
    sdr.sample_rate = sampling_rate
    sdr.center_freq = center_frequency - offset
    sdr.gain = gain

    async for samples in sdr.stream(blocksize):
        if interrupt:
            break
        await audioqueue.put(Sample(samples).audio_mono(sampling_rate, offset))

    try:
        await sdr.stop()
    except Exception:
        pass

    sdr.close()


async def read_and_play(
    input_path_or_frequency: Union[int, Path],
    *,
    blocksize: int,
    gain: Union[Literal["auto"], int],
    offset: Hertz,
    output: Optional[Path] = None,
):
    "Lecture des données pour écoute."

    def switch_interrupt():
        global interrupt
        interrupt = True

    loop = asyncio.get_event_loop()
    loop.add_signal_handler(signal.SIGINT, switch_interrupt)

    audioqueue: asyncio.Queue[np.ndarray] = asyncio.Queue()
    ajustement = None

    if output:
        output_fh = sf.SoundFile(output, "w", channels=1, samplerate=44100)

    def callback(outdata, frames, time, status):
        nonlocal ajustement
        try:
            data = audioqueue.get_nowait()

            # On ne fait l'ajustement du volume qu'une seule fois
            if ajustement is None:
                ajustement = 10000 / np.max(
                    np.abs(data)
                )  # ajustement du volume
            data *= ajustement
            audioqueue.task_done()
            outdata[:, 0] = data

            if output:
                output_fh.write(data.astype(np.int16))

        except asyncio.QueueEmpty:  # Rien n'est encore arrivé
            outdata.fill(0)
        except ValueError:
            # Probablement la fin d'un fichier: on tombe rarement juste!
            outdata.fill(0)
            outdata[: data.size, 0] = data

    with sd.OutputStream(
        samplerate=44100,
        blocksize=int(blocksize / 25),
        channels=1,
        dtype="int16",
        callback=callback,
    ):
        if isinstance(input_path_or_frequency, int):
            await sdr_streaming(
                audioqueue,
                center_frequency=input_path_or_frequency,
                blocksize=blocksize,
                offset=offset,
                gain=gain,
            )
        else:
            await file_streaming(
                audioqueue,
                file=input_path_or_frequency,
                blocksize=blocksize,
                offset=offset,
            )

        # on attend que la file se vide pour arrêter...
        while not interrupt and audioqueue.qsize():
            await asyncio.sleep(0.1)

    if output:
        output_fh.close()


# Outillage de l'interface en ligne de commande CLI
# Voir chapitre 21:
#   « Comment écrire un outil graphique ou en ligne de commande ? »


def validate_gain(ctx, param, value) -> Union[Literal["auto"], int]:
    msg = "Le paramètre gain doit être un entier ou 'auto'"
    if value == "auto":
        return value
    try:
        return int(value)
    except:
        raise click.BadParameter(msg)


def validate_frequency_or_offset(ctx, param, value):
    msg = "La fréquence doit être entière. Les raccourcis 103.1M et 200k sont valides."
    try:
        if match := re.match(r"\s*(-?[\d.]+)[Mm]", value):
            return int(float(match.group(1)) * 1e6)
        if match := re.match(r"\s*(-?[\d.]+)[Kk]", value):
            return int(float(match.group(1)) * 1e3)
        return int(value)
    except:
        raise click.BadParameter(msg)


def validate_path_or_frequency(ctx, param, value):
    if (path := Path(value)).exists() and path.is_file():
        return path
    return validate_frequency_or_offset(ctx, param, value)


description = """
Il est possible de lire des données depuis un fichier binaire
ou directement depuis une fréquence FM.

Exemples d'utilisation:\n
$ python fmradio.py 103.5M

Pour un offset (optionnel) négatif:\n
$ python fmradio.py samples.rtl --offset ' -200k'
"""


@click.command(help=description)
@click.option("-b", "--blocksize", show_default=True, default=1_024_000)
@click.option(
    "-g",
    "--gain",
    default="auto",
    show_default=True,
    callback=validate_gain,
)
@click.option("-o", "--output", type=click.Path(), default=None)
@click.option(
    "--offset",
    type=str,
    default="200k",
    show_default=True,
    callback=validate_frequency_or_offset,
)
@click.argument("input_path_or_frequency", callback=validate_path_or_frequency)
def main(
    input_path_or_frequency: Union[int, Path],
    offset: Hertz,
    gain: Union[Literal["auto"], int],
    blocksize: int,
    output: Optional[Path],
):

    # L'utilisation d'uvloop offre de meilleures performances
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())
    asyncio.run(
        read_and_play(
            input_path_or_frequency,
            blocksize=blocksize,
            offset=offset,
            gain=gain,
            output=output,
        )
    )


if __name__ == "__main__":
    main()
