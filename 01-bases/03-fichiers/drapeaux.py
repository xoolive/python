import json
from operator import itemgetter
from pathlib import Path
from zipfile import ZipFile

# Les fichiers sont téléchargeables sur flagpedia.net
# https://flagcdn.com/w2560.zip
# https://flagcdn.com/fr/codes.json

data_dir = Path(__file__).parent.parent.parent / "data"
country_file = data_dir / "codes.json"
zip_file = data_dir / "w2560.zip"

countries = json.loads(country_file.read_text())


def lire_entier(x: bytes) -> int:
    """Convertit une séquence bytes en entier.

    >>> lire_entier(b"\x01\x00")
    256
    """
    return int.from_bytes(x, byteorder="big")


def lire_png(fh, drapeau: dict) -> None:

    # Les 8 premiers bits sont la signature b"\x89PNG\r\n\x1a\n"
    signature = fh.read(8)

    # Le fichier est ensuite découpé en "chunks"
    chunk_type = b""
    while chunk_type != b"IEND":

        # Un chunk est constitué de 4 bits de taille, 4 bits de type,
        # puis des données, et enfin 4 bits d'un code correcteur d'erreur
        length = lire_entier(fh.read(4))
        chunk_type = fh.read(4)
        chunk_data = fh.read(length)
        crc = fh.read(4)

        # On récupère la taille de l'image dans le header (chunk IHDR)
        if chunk_type == b"IHDR":
            drapeau["largeur"] = lire_entier(chunk_data[:4])
            drapeau["hauteur"] = lire_entier(chunk_data[4:8])
            drapeau["L×h"] = drapeau["largeur"] * drapeau["hauteur"]

        # On récupère la taille de la partie compressée de l'image (chunk IDAT)
        if chunk_type == b"IDAT":
            drapeau["taille_png"] = length

    # Enfin, on calcule quelques ratios de compression
    drapeau["png_ratio"] = drapeau["L×h"] / drapeau["taille_png"]
    drapeau["zip_ratio"] = drapeau["taille_png"] / drapeau["taille_zip"]


with ZipFile(zip_file.as_posix(), "r") as zf:
    all_files = []

    # On ouvre chaque fichier de l'archive
    for file_info in zf.infolist():
        with zf.open(file_info.filename, "r") as fh:

            # On récupère le nom du fichier, le nom du pays,
            # et la taille du PNG dans l'archive

            drapeau = {
                "fichier": file_info.filename,
                "taille_zip": file_info.compress_size,
                "pays": countries[file_info.filename[:-4]],
            }
            lire_png(fh, drapeau)
            all_files.append(drapeau)


list_files = sorted(all_files, key=itemgetter("png_ratio"))

# Code supplémentaire pour affichage du résultat dans le terminal

from rich.console import Console
from rich.table import Table

console = Console()
table = Table(show_header=True, header_style="bold magenta")
table.add_column("Fichier")
table.add_column("Pays")
table.add_column("PNG ratio", justify="right")
table.add_column("ZIP ratio", justify="right")

for elt in list_files[:5]:
    table.add_row(
        elt["fichier"],
        elt["pays"],
        f"{elt['png_ratio']:.2f}",
        f"{elt['zip_ratio']:.2f}",
    )

table.add_row()

for elt in list_files[-5:]:
    table.add_row(
        elt["fichier"],
        elt["pays"],
        f"{elt['png_ratio']:.2f}",
        f"{elt['zip_ratio']:.2f}",
    )

console.print(table)
