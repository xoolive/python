---
title: Installation de l'environnement
permalink: /installation
back: /python
---

La première partie du livre _Les bases du langage Python_ ne nécessite pas d'environnement particulier. N'importe quelle installation Python de base dont la version est supérieure à 3.12 suffira.

<div class="alert alert-danger">
  Au delà, l'environnement Pixi, qui facilite l'accès aux distributions Anaconda, est fortement recommandé.
</div>

## Installation de l'environnement

Si l'outil `git` est déjà installé, vous pouvez au préalable copier les ressources du livre:

```sh
git clone https://github.com/xoolive/python
cd python
pixi run python
```

Sinon, l'installation de l'environnement donne également accès à l'outil `git`.

## Utilisation de l'environnement

Avant chaque utilisation, entrer dans un terminal (ou une invite de commandes Powershell sous Windows) la commande suivante:

```sh
pixi shell
```

On peut aussi préfixer chaque commande avec `pixi run`:

```sh
pixi run jupyter lab
```
