---
permalink: /packaging/
title: Chapitre 22
back: /python/contents
---

## 22. Publier une bibliothèque Python

Le code de la bibliothèque `fip_online` est fourni dans le github du livre.

Si cela n'a pas [déjà été fait](https://www.xoolive.org/python/installation), commencer par cloner le repository GitHub:

```bash
git clone https://github.com/xoolive/python
```

Puis, se rendre dans le dossier du chapitre et installer la bibliothèque:

```bash
cd python/05-projects/22-packaging/fip_online
pip install .
```

Les trois outils proposés sont alors les suivants:

```bash
fip_web  # un service web en Flask
fip_online  # un client en ligne de commande avec click
fip_gui  # une interface graphique en Qt
```

### 22.1 Le packaging Python selon le PEP 517

### 22.2 La gestion des fichiers de configuration

### 22.3 Publier du code source

### 22.4 Publier des paquets Python
