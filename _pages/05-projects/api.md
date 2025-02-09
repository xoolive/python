---
permalink: /api/
title: Chapitre 28
back: /python/contents
---

## 28. Comment écrire une API Python vers une bibliothèque C?

### 28.1 Optimiser un code avec Numba et Cython

Télécharger le notebook [![ipynb](https://img.shields.io/badge/-Jupyter-F37626?logo=jupyter&logoColor=white)](https://raw.githubusercontent.com/xoolive/python/master/05-projects/28-api/numba_cython.ipynb)

### 28.2 Écrire une API Python pour une bibliothèque C

Le code de la bibliothèque `freetype` est fourni dans le github du livre.

Si cela n'a pas [déjà été fait](https://www.xoolive.org/python/installation), commencer par cloner le repository GitHub:

```bash
git clone https://github.com/xoolive/python
```

Puis, se rendre dans le dossier du chapitre et installer la bibliothèque:

```bash
cd python/05-projects/28-api/freetype
pip install .
```

Exécuter le programme suivant pour obtenir une fenêtre Matplotlib comme ci-dessous.

```bash
python sample.py
```

![Résultat graphique](https://raw.githubusercontent.com/xoolive/python/master/05-projects/28-api/freetype/sample.png)

### 28.3. Écrire un binding Rust avec maturin

Se rendre dans le dossier du chapitre:

```bash
cd python/05-projects/28-api/pywhatlang
uv run python
```

puis dans l'interpréteur:

```python
>>> from pywhatlang import detect
>>> detect("J'apprends à programmer en Python et en Rust.")
'{"lang":"fra","script":"Latin","confidence":0.4401946958305268}'
>>> detect("I am learning to program in Python and Rust.")
'{"lang":"eng","script":"Latin","confidence":0.9944095797574993}'
>>> detect("Jag lär mig att programmera i Python och Rust")
'{"lang":"swe","script":"Latin","confidence":1.0}'
>>> detect("저는 Python과 Rust로 프로그래밍하는 법을 배우고 있어요.")
'{"lang":"kor","script":"Hangul","confidence":1.0}'
>>> detect("Уча се да програмирам на Python и Rust.")
'{"lang":"bul","script":"Cyrillic","confidence":0.0227157036337226}'
>>> detect("ฉันกำลังเรียนรู้การเขียนโปรแกรมด้วย Python และ Rust")
'{"lang":"tha","script":"Thai","confidence":1.0}'
```
