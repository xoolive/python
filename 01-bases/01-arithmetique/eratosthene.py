def crible_eratosthene(n: int) -> set:
    "Énumère les nombres premiers inférieurs à n."

    # On crée d'abord la grille complète
    p = set(range(2, n))
    # puis pour chaque entier i,
    for i in range(2, n):
        # on élimine l'ensemble des multiples de i
        p = p - set(x * i for x in range(2, n // i + 1))
    return p


print(crible_eratosthene(20))
