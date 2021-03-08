---
permalink: /iteration/syracuse
title: La suite de Syracuse
back: /python/iteration/
layout: code
partie: 03-pythonic
chapitre: 14-iteration
code: syracuse.py
---

Comme la suite de Fibonacci, la suite de Syracuse est un bon exemple pour illustrer le fonctionnement des fonctions qui renvoient des générateurs. La suite de Syracuse démarre sur un entier positif. À chaque itération, si le dernier entier est pair, on renvoie le résultat de sa division par 2; sinon on le multiplie par 3 avant d'ajouter 1.

Une conjecture prédit que cette suite converge systématiquement vers 1. 1 étant impair, les valeurs suivantes sont 4, puis 2, puis 1: aussi l'usage est d'interrompre cette suite quand la valeur 1 est atteinte.

Les résultats intéressants pour cette suite peuvent être:

- la séquence complète de valeurs qui démarrent à un entier donné

![Parcours de la suite de Syracuse](/python/_static/syracuse_27.png){: class="rendu_code"}

- la longueur de cette suite: combien faut-il d'itérations pour atteindre la valeur 1?

![Longueur de la suite de Syracuse](/python/_static/syracuse_length.png){: class="rendu_code"}

- la hauteur de cette suite: quelle est la valeur maximale atteinte par la suite avant de converger vers 1?

![Hauteur de la suite de Syracuse](/python/_static/syracuse_height.png){: class="rendu_code"}
