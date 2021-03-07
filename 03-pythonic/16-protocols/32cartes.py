import itertools
from dataclasses import dataclass


@dataclass
class Carte:
    valeur: str
    couleur: str

    def __repr__(self):
        return f"{self.valeur}{self.couleur}"


class Jeu32Cartes:
    couleurs = ["♠", "♥", "♦", "♣"]
    valeurs = ["A", "R", "D", "V", "10", "9", "8", "7"]

    def __init__(self):
        self._ensemble = list(
            Carte(valeur, couleur)
            for (valeur, couleur) in itertools.product(self.valeurs, self.couleurs)
        )

    def __iter__(self):
        yield from self._ensemble

    def __len__(self):
        return len(self._ensemble)

    def __contains__(self, value):
        return Carte(value[:-1], value[-1]) in iter(self)


print(f"{list(Jeu32Cartes()) = }")
print(f"{len(Jeu32Cartes()) = }")
print(f"{'10♠' in Jeu32Cartes() = }")
