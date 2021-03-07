from collections import deque
from dataclasses import dataclass, field
from functools import partial, reduce
from itertools import count
from typing import List

import matplotlib.pyplot as plt
import numpy as np

# Définition des types

radians = float


@dataclass(frozen=True)
class LSystem:
    axiom: str  # l'axiome de départ
    rules: "dict[lettre, str]"  # les règles de réécriture
    order: int  # combien de fois appliquer les règles
    draw: "dict[str, turtle -> turtle]"  # les règles de dessin


@dataclass(frozen=True)  # programmation fonctionnelle: rien n'est mutable!
class Tortue:
    positions: List[np.ndarray] = field(
        default_factory=lambda: [[np.array([0, 0], dtype=float)]]
    )
    orientation: np.ndarray = np.array([[0], [1]], dtype="float")
    pile: deque = field(default=deque())


# Définition des règles de réécriture


def rewrite_rules(rules: "dict[lettre, str]") -> "str, * -> str":
    """Réécriture d'un L-système.

    Cette fonction renvoie une fermeture capable d'appliquer les règles
    de réécriture passée au paramètre `rules` sur une chaîne de caractères.

    Si une lettre n'est pas présente dans les règles de réécriture, elle
    est recopiée telle quelle.

    >>> rewrite_rules(rules = dict(A="B", B="AA"))("ACAB")
    "BCBAA"

    """

    def apply_rule(lettre: "lettre") -> "str":
        return rules.get(lettre, lettre)  # ①

    def rewrite(seq: str, *args) -> str:
        # return "".join(apply_rule(lettre) for lettre in seq)
        return "".join(map(apply_rule, seq))

    return rewrite  # ②


def drawing_rules(
    rules: "dict[str, Tortue -> Tortue]",
) -> "Tortue, str -> Tortue":
    def identite(x):
        return x

    def deplace_tortue(tortue: Tortue, action: str) -> Tortue:
        return rules.get(action, identite)(tortue)

    return deplace_tortue


def lsystem(definition: LSystem) -> np.ndarray:

    tortue = Tortue()

    actions: str = reduce(
        # str, int ->str
        rewrite_rules(definition.rules),
        # Sequence[int]
        range(definition.order),
        # str
        definition.axiom,
    )

    tortue = reduce(
        # turtle, str -> turtle
        drawing_rules(definition.draw),
        # str
        actions,
        # turtle
        Tortue(),
    )

    return np.vstack(tortue.positions)


# Déplacements de la tortue graphique


def avance(tortue: Tortue) -> Tortue:
    return Tortue(
        tortue.positions + [tortue.positions[-1] + tortue.orientation.T],
        tortue.orientation,
        tortue.pile,
    )


def rotation(angle: radians, tortue: Tortue) -> Tortue:
    mat = np.array(
        [[np.cos(angle), -np.sin(angle)], [np.sin(angle), np.cos(angle)]]
    )
    return Tortue(tortue.positions, mat @ tortue.orientation, tortue.pile)


def empile(tortue: Tortue) -> Tortue:
    pile = tortue.pile
    pile.append((tortue.positions[-1], tortue.orientation))
    return Tortue(tortue.positions, tortue.orientation, pile)


def depile(tortue: Tortue) -> Tortue:
    pile = tortue.pile
    position, orientation = pile.pop()
    nan_position = np.array([[np.nan, np.nan]])
    return Tortue(
        tortue.positions + [nan_position, position], orientation, pile
    )


# Définitions de L-systèmes

courbe_de_koch = LSystem(
    axiom="F",
    rules=dict(F="F+F-F-F+F"),
    order=3,
    draw={
        "F": avance,
        "+": partial(rotation, np.radians(90)),
        "-": partial(rotation, -np.radians(90)),
    },
)
serpinsky = LSystem(
    axiom="F+G+G",
    rules=dict(F="F+G-F-G+F", G="GG"),
    order=5,
    draw={
        "F": avance,
        "G": avance,
        "-": partial(rotation, -np.radians(120)),
        "+": partial(rotation, np.radians(120)),
    },
)

bushy_tree = LSystem(
    axiom="F",
    rules=dict(F="FF-[-F+F+F]+[+F-F-F]"),
    order=3,
    draw={
        "F": avance,
        "-": partial(rotation, -np.radians(25)),
        "+": partial(rotation, np.radians(25)),
        "[": empile,
        "]": depile,
    },
)

hilbert = LSystem(
    rules=dict(L="-RF+LFL+FR-", R="+LF-RFR-FL+"),
    axiom="L",
    order=4,
    draw={
        "F": avance,
        "-": partial(rotation, -np.radians(90)),
        "+": partial(rotation, np.radians(90)),
    },
)

flow_snake = LSystem(
    axiom="L",
    rules=dict(
        L="L-R--R+L++LL+R-",
        R="+L-RR--R-L++L+R",
    ),
    order=3,
    draw={
        "L": avance,
        "R": avance,
        "-": partial(rotation, -np.radians(60)),
        "+": partial(rotation, np.radians(60)),
    },
)

crystal = LSystem(
    axiom="B",
    rules=dict(A="BA+HA+B-A", B="B+A-B-JBA", H="-", J="+"),
    order=4,
    draw={
        "A": avance,
        "B": avance,
        "-": partial(rotation, -np.radians(90)),
        "+": partial(rotation, np.radians(90)),
    },
)

# Affichage dans Matplotlib


designs = [courbe_de_koch, serpinsky, bushy_tree, hilbert, flow_snake, crystal]

fig, ax = plt.subplots(2, 3, figsize=(13, 7))
for i, ax_, design in zip(count(), ax.ravel(), designs):
    x, y = lsystem(design).T
    if i < 2:  # Rotation pour certains
        ax_.plot(y, -x, "k")
    else:
        ax_.plot(x, y, "k")
    ax_.set_aspect(1)
    ax_.axis("off")

fig.set_tight_layout(True)

fig.savefig("lsystems.png")
plt.show()
