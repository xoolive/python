import doctest


def pgcd(a, b):
    """Calcule le PGCD de deux entiers positifs
    Si nécessaire, les nombres passés sont convertis en entier.
    >>> pgcd(12, 8)
    3
    >>> pgcd("4", 2.4)  # conversion en entier
    2
    >>> pgcd(12, -8)
    Traceback (most recent call last):
    ...
    ValueError: Les deux entiers doivent être positifs"""

    a, b = int(a), int(b)

    if a < 0 or b < 0:
        raise ValueError("Les deux entiers doivent être positifs")

    while a != b:
        if a > b:
            a = a - b
        else:
            b = b - a
    return a


if __name__ == "__main__":
    doctest.testmod()