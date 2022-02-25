from collections import namedtuple
from math import sin, cos, radians
from pathlib import Path

Node = namedtuple("Node", "name angle")  # description du type Node

distances = dict()  # ①
distances["Juvisy", "Villejuif"] = 5748  # ②
distances["Sig.Nord", "Sig.Sud"] = 7928 + 5 / 6

with Path("../../data/cassini/triangles.txt").open("r") as fh:
    # Cette liste va stocker les valeurs intermédiaires par triangle
    triangle = list()

    for line in fh.readlines():
        line = line.strip()  # on supprime les espaces inutiles
        if line == "":  # on ignore alors les lignes vides
            continue

        name, deg, mn, sec = line.split()  # ⑤
        angle = float(deg) + float(mn) / 60 + float(sec) / 3600  # ③
        triangle.append(Node(name, radians(angle)))

        if len(triangle) == 3:  # ④
            n1, n2, n3 = triangle  # ⑤

            d3 = distances.get((n1.name, n2.name), None)  # ⑥
            if d3 is None:  # si d[n1, n2] n'est pas disponible, d[n2, n1] le sera
                d3 = distances.get((n2.name, n1.name))

            distances[n1.name, n3.name] = sin(n2.angle) * d3 / sin(n3.angle)
            distances[n2.name, n3.name] = sin(n1.angle) * d3 / sin(n3.angle)
            # on vide la liste
            triangle.clear()


with Path("../../data/cassini/inclinaisons.txt").open("r") as fh:
    # On stocke dans total la longueur de la méridienne (en toises)
    total = 0

    for line in fh.readlines():
        line = line.strip()  # on supprime les espaces inutiles
        if line == "":  # on ignore alors les lignes vides
            continue

        n1, n2, deg, mn, sec = line.split()  # ⑦
        angle = float(deg) + float(mn) / 60 + float(sec) / 3600
        angle = radians(angle)
        d = distances.get((n1, n2), None)
        if d is None:  # si d[n1, n2] n'est pas disponible, d[n2, n1] le sera
            d = distances.get((n2, n1))
        total += d * cos(angle)  # ⑧

    total *= 1.949  # ⑨

latitudes = [
    [2, 11, 50, 17],  # Dunkerque -- Observatoire
    [1, 45, 7, 20],  # Observatoire -- Bourges
    [2, 43, 51, 5],  # Bourges -- Rodez
    [1, 39, 11, 12],  # Perpignan -- Rodez
]

# On somme alors les angles ⑩
angle = sum(a[0] for a in latitudes)  # degrés
angle += sum(a[1] for a in latitudes) / 60  # minutes
angle += sum(a[2] for a in latitudes) / 3600  # secondes
angle += sum(a[3] for a in latitudes) / 216000  # tierces

print("Rayon de la terre: {:.4g} km".format(total / radians(angle) / 1000))
