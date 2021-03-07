---
permalink: /structures/polonaise
title: La notation polonaise inverse
back: /python/structures
layout: code
partie: 01-bases
chapitre: 04-structures
code: polonaise.py
---

La notation polonaise inverse est une pratique d'écriture d'opérations arithmétiques, populaire dans les années 1960, qui permet de ne pas utiliser de parenthèses. Les opérateurs arithmétiques sont utilisés en position *suffixe*.

On écrit alors $1\;2\;+$ au lieu de $1 + 2$.

Cette notation permet d'*empiler* des opérations et des résultats intermédiaires. Ainsi, on écrira $1\;2 + 3\;\times$ pour $(1 + 2) \times 3$: le résultat intermédiaire de l'opération $(1 + 2)$ est *empilé* avant d'être utilisé dans l'opération de multiplication suivante. Avec un ordre de priorité différent, l'opération $1+(2\times 3)$ s'écrit $1\;2\;3\times+$.

La structure de deque permet d'empiler des opérations pour interpréter une séquence écrite en notation polonaise inverse:
- les nombres (ici entiers) sont simplement empilés avec l'opération `.append()`;
- les opérateurs (ici chaînes de caractères) dépilent avec l'opération `.pop()` les deux dernières valeurs de la pile, évaluent l'opération et empilent le résultat.
