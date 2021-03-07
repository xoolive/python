---
permalink: /structures/jeux_de_des
title: Jeux de dés
back: /python/structures
---

La programmation et les générateurs aléatoires des ordinateurs sont de bons outils pour mettre en évidence des lois statistiques simples. L'exemple ici est inspiré d'une publication Twitter de [Raymond Hettinger](https://twitter.com/raymondh).

Nous allons utiliser l'ordinateur pour lancer des dés, puis utiliser la structure de dictionnaire de dénombrement `Counter` pour compter le nombre d'occurrences de configurations particulières. On peut définir un « jeu » comme un critère associé à une combinaison de valeurs données par les dés.

Nous allons définir les « jeux » suivants:
- on lance deux dés, puis on somme les chiffres;
- on lance cinq dés, puis on garde celui au deuxième plus petit chiffre.

À titre d'exercice, le lecteur pourra coder d'autres jeux à base de cinq dés: par exemple, en comptant le nombre de dés identiques parmi cinq dés lancés, ou en calculant la différence entre la plus grande et la plus petite valeur sur les dés.

<script src="https://emgithub.com/embed.js?target=https%3A%2F%2Fgithub.com%2Fxoolive%2Fpython%2Fblob%2Fmaster%2F01-bases%2F04-structures%2Fjeux_de_des.py&style=github-gist&showLineNumbers=on"></script>