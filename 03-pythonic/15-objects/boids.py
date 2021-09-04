from typing import Iterable

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation, path

radians = float

boid_shape = path.Path(
    # coordonnées du schéma ci-dessous, orienté vers la droite
    vertices=np.array([[0, 0], [-100, 100], [200, 0], [-100, -100], [0, 0]]),
    codes=np.array([1, 2, 2, 2, 79], dtype=np.uint8),
)


def rotate_marker(p: path.Path, angle: radians) -> path.Path:
    cos, sin = np.cos(angle), np.sin(angle)
    newpath = p.vertices @ (np.array([[cos, sin], [-sin, cos]]))
    return path.Path(newpath, p.codes)


class Boid:

    taille = 300
    max_voisins = 10

    def __init__(self, position=None, vitesse=None) -> None:
        self.x = (
            position
            if position is not None
            else np.random.uniform(-Boid.taille, Boid.taille, 2)
        )
        self.dx = (
            vitesse if vitesse is not None else np.random.uniform(-5, 5, 2)
        )

    def __repr__(self) -> str:
        return f"Boid({self.x.round(2)}, {self.dx.round(2)})"

    @property
    def vitesse(self) -> float:
        return np.linalg.norm(self.dx)

    @vitesse.setter
    def vitesse(self, value: float) -> None:
        self.dx = self.dx * value / self.vitesse

    @property
    def direction(self) -> "radians":
        return np.arctan2(self.dx[1], self.dx[0])

    def distance(self, other: "Boid") -> float:
        "Renvoie la distance entre deux Boid"
        return np.linalg.norm(self.x - other.x)

    def angle_mort(self, other: "Boid") -> bool:
        "Renvoie True si le Boid `other` est dans l'angle mort du Boid courant."
        v1 = self.dx - self.x
        v2 = other.dx - other.x
        cos_angle = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        return np.arccos(cos_angle) > 0.75 * np.pi

    def voisins(
        self, population: "Iterable[Boid]", seuil: float
    ) -> "list[Boid]":
        "Renvoie la liste des voisins visibles, triés par ordre croissant de distance."
        return sorted(
            (
                other
                for other in population
                if self is not other
                and not self.angle_mort(other)
                and self.distance(other) < seuil
            ),
            key=self.distance,
        )

    def separation(self, population: "Iterable[Boid]"):
        "La composante de la force qui éloigne les Boids les uns des autres."
        return sum(
            self.x - other.x
            for other in self.voisins(population, 50)[: Boid.max_voisins]
        )

    def align(self, population: "Iterable[Boid]"):
        "La composante de la force qui aligne les Boids les uns avec les autres"
        voisins = self.voisins(population, 200)[: Boid.max_voisins]
        vitesses = sum(other.dx for other in voisins)
        return vitesses / len(voisins) - self.dx if len(voisins) else 0

    def cohere(self, population):
        "La composante de la force qui rapproche les Boids les uns des autres."
        voisins = self.voisins(population, 200)[: Boid.max_voisins]
        vitesses = sum(other.x for other in voisins)
        return vitesses / len(voisins) - self.x if len(voisins) else 0

    def centripete(self):
        "Une composante de force centripète."
        return -self.x

    def noise(self):
        "Un peu de comportement imprévisible."
        return np.random.uniform(-5, 5, 2)

    def interaction(self, population: "Iterable[Boid]") -> "Boid":
        "On déplace le Boid en fonction de toutes les forces qui s'y appliquent"

        self.dx += (  # avec des pondérations respectives
            self.separation(population) / 10
            + self.align(population) / 8
            + self.cohere(population) / 100
            + self.centripete() / 200
            # + self.noise()
        )

        # Les Boids ne peuvent pas aller plus vite que la musique
        if self.vitesse > 20:
            self.vitesse = 20

        # On avance
        self.x += self.dx

        # On veille à rester dans le cadre par effet rebond
        if (np.abs(self.x) > Boid.taille).any():
            for i, coord in enumerate(self.x):
                if (diff := coord + Boid.taille) < 10:
                    self.x[i] = -Boid.taille + 10 + diff
                    self.dx[i] *= -1
                if (diff := Boid.taille - coord) < 10:
                    self.x[i] = Boid.taille - 10 - diff
                    self.dx[i] *= -1

        return self


class Simulation:
    def __init__(self, n: int, ax, seed: int = 2042) -> None:

        np.random.seed(seed)

        self.boids = list(Boid() for _ in range(n))
        self.artists = list()
        self.plot(ax)

    def plot(self, ax) -> None:

        for boid in self.boids:
            p, *_ = ax.plot(
                *boid.x,
                color=".1",
                markersize=15,
                marker=rotate_marker(boid_shape, boid.direction),
            )
            self.artists.append(p)

        ax.set_xlim((-Boid.taille, Boid.taille))
        ax.set_ylim((-Boid.taille, Boid.taille))
        ax.set_aspect(1)
        ax.xaxis.set_visible(False)
        ax.yaxis.set_visible(False)

    def iteration(self, _i: int):
        self.boids = list(boid.interaction(self.boids) for boid in self.boids)

        for p, boid in zip(self.artists, self.boids):
            p.set_data(*boid.x)
            p.set_marker(rotate_marker(boid_shape, boid.direction))

        return self.artists


fig, ax = plt.subplots(figsize=(7, 7))
simulation = Simulation(n=100, ax=ax)

anim = animation.FuncAnimation(
    fig,
    simulation.iteration,
    frames=range(0, 200),
    interval=150,
    blit=True,
    repeat=True,
)

anim.save("boids.mp4")
