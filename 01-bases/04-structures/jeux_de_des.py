from collections import Counter
from random import choices

faces = range(1, 7)  #  les 6 faces d'un dé


def somme_de_deux_dés() -> int:
    # on tire 2 dés, on fait la somme
    return sum(choices(faces, k=2))


def deuxième_plus_petit() -> int:
    # on tire 5 dés, on les trie dans l'ordre pour ne garder que le 2e
    return sorted(choices(faces, k=5))[1]


def statistiques(jeu, nombre_jets=200) -> dict:
    return Counter(jeu() for _ in range(nombre_jets))


print(statistiques(somme_de_deux_dés))
print(statistiques(deuxième_plus_petit))
