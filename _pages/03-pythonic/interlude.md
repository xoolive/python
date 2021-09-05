---
permalink: /fmradio/
title: Interlude
back: /python/contents
---

## Interlude -- La démodulation de signaux FM

- Installer [Git LFS](https://git-lfs.github.com/) si ce n'est déjà fait;
- Entrer la commande `git lfs pull` pour télécharger le fichier `sample.rtl`
- Vérifier la taille du fichier (57Mb) et son shasum `fb548e763cdc92ab84a0ce126eb81395ae03733c`

Le script `fmradio.py` permet de décoder le contenu du fichier:

```zsh
python fmradio.py ../data/samples.rtl
```

<audio src="../_static/moon_river.ogg" controls></audio>

La deuxième piste audio est accessible en changeant le paramètre d'offset:

```zsh
python fmradio.py ../data/samples.rtl --offset ' -200k'
```

<audio src="../_static/gnossienne.ogg" controls></audio>

Si vous avez un [dongle SDR](https://www.rtl-sdr.com/buy-rtl-sdr-dvb-t-dongles/) à portée de main, vous pouvez décoder la radio en temps réel:

```zsh
python fmradio.py 103.5M
```
