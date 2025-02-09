from dataclasses import dataclass
from functools import reduce
from typing import Callable

import tortle
from js import console, document

lettre = str


def rewrite_rules(rules: dict[lettre, str]) -> Callable[[str], str]:
    """Réécriture d'un L-système.

    Cette fonction renvoie une fonction capable d'appliquer les règles
    de réécriture passée au paramètre `rules` sur une chaîne de caractères.

    Si une lettre n'est pas présente dans les règles de réécriture, elle
    est recopiée telle quelle.

    >>> rewrite_rules(rules = dict(A="B", B="AA"))("ACAB")
    "BCBAA"
    """

    def apply_rule(lettre: "lettre") -> str:
        # dict.get(clé, valeur_par_défaut)
        return rules.get(lettre, lettre)  # ①

    def rewrite(seq: str, *args) -> str:
        # return "".join(apply_rule(lettre) for lettre in seq)
        return "".join(map(apply_rule, seq))

    return rewrite  # ②


@dataclass(frozen=True)
class LSystem:
    axiom: str  # l'axiome de départ
    rules: "dict[lettre, str]"  # les règles de réécriture
    order: int  # combien de fois appliquer les règles
    draw: dict[str, Callable[[tortle.Turtle], None]]  # les règles de dessin


courbe_de_koch = LSystem(
    axiom="F",
    rules=dict(F="F+F-F-F+F"),
    order=3,
    draw={
        "F": lambda tortue: tortue.forward(10),
        "+": lambda tortue: tortue.left(90),
        "-": lambda tortue: tortue.right(90),
    },
)

sierpinsky = LSystem(
    axiom="F+G+G",
    rules=dict(F="F+G-F-G+F", G="GG"),
    order=5,
    draw={
        "F": lambda tortue: tortue.forward(10),
        "G": lambda tortue: tortue.forward(10),
        "+": lambda tortue: tortue.left(120),
        "-": lambda tortue: tortue.right(120),
    },
)

hilbert = LSystem(
    rules=dict(L="-RF+LFL+FR-", R="+LF-RFR-FL+"),
    axiom="L",
    order=4,
    draw={
        "F": lambda tortue: tortue.forward(10),
        "-": lambda tortue: tortue.right(90),
        "+": lambda tortue: tortue.left(90),
    },
)

snow_flake = LSystem(
    axiom="L",
    rules=dict(
        L="L-R--R+L++LL+R-",
        R="+L-RR--R-L++L+R",
    ),
    order=3,
    draw={
        "L": lambda tortue: tortue.forward(10),
        "R": lambda tortue: tortue.forward(10),
        "-": lambda tortue: tortue.right(60),
        "+": lambda tortue: tortue.left(60),
    },
)

crystal = LSystem(
    axiom="B",
    rules=dict(A="BA+HA+B-A", B="B+A-B-JBA", H="-", J="+"),
    order=4,
    draw={
        "A": lambda tortue: tortue.forward(10),
        "B": lambda tortue: tortue.forward(10),
        "-": lambda tortue: tortue.right(90),
        "+": lambda tortue: tortue.left(90),
    },
)


def lsystem(definition: LSystem, ma_tortue: tortle.Turtle, ordre: int) -> None:
    actions = reduce(
        rewrite_rules(definition.rules),  # type: ignore
        range(ordre),
        definition.axiom,
    )
    for action in actions:
        definition.draw.get(action, lambda _: ())(ma_tortue)


FRACTALES = {
    "koch": courbe_de_koch,
    "sierpinsky": sierpinsky,
    "hilbert": hilbert,
    "crystal": crystal,
    "snow_flake": snow_flake,
}


def tracer(event):
    console.log(event)

    ordre = int(document.querySelector("#ordre").value)

    tortle.Screen().restart()
    ma_tortue = tortle.Turtle()
    ma_tortue.speed(10)
    lsystem(FRACTALES[event.target.value], ma_tortue, ordre)
    tortle.done(target=document.querySelector("#dessin"))

    # Petit bricolage pour recentrer la fractale à l'intérieur de la balise SVG
    svg = document.querySelector("#dessin").children[0]
    bbox = svg.getBBox()
    x = bbox.x
    y = bbox.y
    width = bbox.width * 1.2
    height = bbox.height * 1.2
    svg.setAttribute("viewBox", f"{x} {y} {width} {height}")
