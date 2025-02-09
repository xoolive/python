---
permalink: /packaging/
title: Chapitre 25
back: /python/contents
---

## 25. Publier une bibliothèque Python

Le code de la bibliothèque `fip_online` est fourni dans le github du livre.

Si cela n'a pas [déjà été fait](https://www.xoolive.org/python/installation), commencer par cloner le repository GitHub:

```bash
git clone https://github.com/xoolive/python
```

Puis, se rendre dans le dossier du chapitre et installer la bibliothèque:

```bash
cd python/05-projects/25-packaging/fip_online  # depuis la v1 du livre
pip install .
```

Les trois outils proposés sont alors les suivants:

```bash
fip_web  # un service web en Flask
fip_online  # un client en ligne de commande avec click
fip_gui  # une interface graphique en Qt
```

L'outil fip_textual est disponible depuis la v2 du livre:

```bash
cd python/05-projects/25-packaging/fip_textual  # depuis la v2 du livre
uv run fip_textual
```

### 25.1 Le packaging Python selon le PEP 517

### 25.2. Le packaging avec l’outil uv

### 25.3. La gestion des fichiers de configuration

### 25.4. Publier du code source

### 25.5. Publier des paquets Python
