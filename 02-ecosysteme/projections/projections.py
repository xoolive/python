from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
import numpy.linalg as la
import scipy.optimize as sopt
from matplotlib import animation

# -- Chargement des données --

villes = [
    "Amsterdam",
    "Athènes",
    "Barcelone",
    "Belgrade",
    "Berlin",
    "Bruxelles",
    "Bucarest",
    "Budapest",
    "Copenhague",
    "Dublin",
    "Gibraltar",
    "Helsinki",
    "Istanbul",
    "Kiev",
    "Kiruna",
    "Lisbonne",
    "Londres",
    "Madrid",
    "Milan",
    "Moscou",
    "Munich",
    "Oslo",
    "Paris",
    "Prague",
    "Reykjavik",
    "Riga",
    "Rome",
    "Sofia",
    "Stockholm",
    "Tallinn",
    "Toulouse",
    "Trondheim",
    "Varsovie",
    "Vienne",
    "Vilnius",
    "Zurich",
]
n = len(villes)  # 32

distances = np.load("../data/distances.npy")
distances /= la.norm(distances)

# -- Fonction d'optimisation et son gradient --


def func(*x):
    """Compute the function to minimise.

    Vector reshaped for more readability.
    """
    res = 0
    x = np.array(x)
    x = x.reshape((n, 2))
    for i in range(n):
        for j in range(i + 1, n):
            (x1, y1), (x2, y2) = x[i, :], x[j, :]
            delta = (x2 - x1) ** 2 + (y2 - y1) ** 2 - distances[i, j] ** 2
            res += delta ** 2
    return res


def func_der(*x):
    r"""Derivative of the preceding function.

    Note: (f \circ g)' = g' \times f' \circ g
    Vector reshaped for more readability.
    """
    res = np.zeros((n, 2))
    x = np.array(x)
    x = x.reshape((n, 2))
    for i in range(n):
        for j in range(i + 1, n):
            (x1, y1), (x2, y2) = x[i, :], x[j, :]
            delta = (x2 - x1) ** 2 + (y2 - y1) ** 2 - distances[i, j] ** 2
            res[i, 0] += 4 * (x1 - x2) * delta
            res[i, 1] += 4 * (y1 - y2) * delta
            res[j, 0] += 4 * (x2 - x1) * delta
            res[j, 1] += 4 * (y2 - y1) * delta
    return np.ravel(res)


# -- Problème d'optimisation --

# Positions initiales au hasard
x0 = np.random.normal(size=(n, 2))

# Normalisation des positions initiales
l1, l2 = np.meshgrid(x0[:, 0], x0[:, 0])
r1, r2 = np.meshgrid(x0[:, 1], x0[:, 1])
x0 /= la.norm(np.sqrt((l1 - l2) ** 2 + (r1 - r2) ** 2))

solution = sopt.fmin_bfgs(func, x0, fprime=func_der, retall=True)

# -- Traitement de la solution --

res = solution[0].reshape((n, 2))

# Rotation: Copenhague est alignée avec Rome
south, north = villes.index("Rome"), villes.index("Copenhague")
d = res[north, :] - res[south, :]
rotate = np.arctan2(d[1], d[0]) - np.pi / 2
mat_rotate = np.array(
    [[np.cos(rotate), -np.sin(rotate)], [np.sin(rotate), np.cos(rotate)]]
)
res = res @ mat_rotate

# Effet miroir: Reykjavik est à l'ouest de Moscou
west, east = villes.index("Reykjavik"), villes.index("Moscou")
mirror = False
if res[west, 0] > res[east, 0]:
    mirror = True
    res[:, 0] *= -1

# On applique la transformation à la trace complète
track = [p.reshape((n, 2)) @ mat_rotate for p in solution[1]]
if mirror:
    track = [p * np.array([-1, 1]) for p in track]

# -- Placement des étiquettes --

d = defaultdict(lambda: {"ha": "left", "va": "bottom"})

for city in [
    "Barcelone",
    "Berlin",
    "Bucarest",
    "Budapest",
    "Istanbul",
    "Reykjavik",
    "Sofia",
    "Tallinn",
    "Vilnius",
    "Riga",
]:
    d[city] = {"ha": "left", "va": "top"}
for city in [
    "Athènes",
    "Londres",
    "Munich",
    "Milan",
    "Stockholm",
    "Zurich",
    "Belgrade",
    "Prague",
]:
    d[city] = {"ha": "right", "va": "top"}
for city in [
    "Copenhagen",
    "Dublin",
    "Munich",
    "Gibraltar",
    "Helsinki",
    "Lisbonne",
    "Madrid",
    "Nantes",
    "Oslo",
    "Paris",
    "Toulouse",
    "Amsterdam",
]:
    d[city] = {"ha": "right", "va": "bottom"}

# -- Visualisation du processus d'optimisation --

fig, ax = plt.subplots(figsize=(10, 10), subplot_kw=dict(aspect=1))

bx = min(res[:, 0]), max(res[:, 0])
dx = bx[1] - bx[0]
ax.set_xlim(bx[0] - 0.1 * dx, bx[1] + 0.1 * dx)

by = min(res[:, 1]), max(res[:, 1])
dy = by[1] - by[0]
ax.set_ylim(by[0] - 0.1 * dy, by[1] + 0.1 * dy)


ax.set_xticklabels([])
ax.set_yticklabels([])
ax.set_axis_off()

ax.set_xlim(bx[0] - 0.1 * dx, bx[1] + 0.1 * dx)
ax.set_ylim(by[0] - 0.1 * dy, by[1] + 0.1 * dy)

# automatic colouring
colors = plt.cm.rainbow(np.linspace(0, 1, n))

p = {}
s = {}
a = {}

tmax = 1

for i, ((_x, _y), city, color) in enumerate(zip(res, villes, colors)):
    t = np.array([t[i, :] for t in track])
    (p[i],) = ax.plot(t[:tmax, 0], t[:tmax, 1], color=color, alpha=0.2)
    (s[i],) = ax.plot(t[tmax - 1, 0], t[tmax - 1, 1], "o", color=color)
    a[i] = ax.annotate(
        "  " + city + "  ",
        (t[tmax - 1, 0], t[tmax - 1, 1]),
        **d[city],
        fontname="Ubuntu",
        fontsize=14,
    )


def init():
    return (*p, *s, *a)


def update(tmax):
    for i, ((_x, _y), _city, _color) in enumerate(zip(res, villes, colors)):
        t = np.array([t[i, :] for t in track])
        p[i].set_data(t[:tmax, 0], t[:tmax, 1])
        s[i].set_data(t[tmax - 1, 0], t[tmax - 1, 1])
        a[i].set_position((t[tmax - 1, 0], t[tmax - 1, 1]))
    return (*p, *s, *a)


anim = animation.FuncAnimation(
    fig, update, len(track), init_func=init, interval=200
)

anim.save("cities.mp4")
