---
permalink: /api/
title: Chapitre 25
back: /python/contents
---

## 25. Comment écrire une API Python vers une bibliothèque C?

### 25.1 Optimiser un code avec Numba et Cython

Télécharger le notebook [![ipynb](https://img.shields.io/badge/-Jupyter-F37626?logo=jupyter&logoColor=white)](https://raw.githubusercontent.com/xoolive/python/master/05-projects/25-api/numba_cython.ipynb)

### 25.2 Écrire une API Python pour une bibliothèque C

Le code de la bibliothèque `freetype` est fourni dans le github du livre.

Si cela n'a pas [déjà été fait](https://www.xoolive.org/python/installation), commencer par cloner le repository GitHub:

```bash
git clone https://github.com/xoolive/python
```

Puis, se rendre dans le dossier du chapitre et installer la bibliothèque:

```bash
cd python/05-projects/25-api/freetype
pip install .
```

Exécuter le programme suivant pour obtenir une fenêtre Matplotlib comme ci-dessous.

```bash
python sample.py
```

![Résultat graphique](https://raw.githubusercontent.com/xoolive/python/master/05-projects/25-api/freetype/sample.png)
