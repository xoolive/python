---
title: Installation de l'environnement
permalink: /installation
back: /python
---

La première partie du livre _Les bases du langage Python_ ne nécessite pas d'environnement particulier. N'importe quelle installation Python de base dont la version est supérieure à 3.8 suffira.

<div class="alert alert-danger">
  Au delà, la distribution Anaconda est fortement recommandée.
</div>

## Installation de l'environnement

Télécharger le fichier [`environment.yml`](https://github.com/xoolive/python/blob/master/environment.yml) puis entrer la commande:

```sh
conda env create -f environment.yml
```

Si l'outil `git` est déjà installé, vous pouvez au préalable copier les ressources du livre:

```sh
git clone https://github.com/xoolive/python
cd python
conda env create -f environment.yml
```

Sinon, l'installation de l'environnement donne également accès à l'outil `git`.

## Utilisation de l'environnement

Avant chaque utilisation, entrer dans un terminal (ou une invite de commandes Anaconda sous Windows) la commande suivante:

```sh
conda activate advancedpython
```

## Installation optimisée de l'environnement

L'outil `mamba` peut se substituer à l'outil `conda`. Il est beaucoup plus performant que `conda` au niveau de la résolution des dépendances et du téléchargement des paquets.

```sh
conda install -n base -c conda-forge mamba
# puis
mamba env create -f environment.yml
```
