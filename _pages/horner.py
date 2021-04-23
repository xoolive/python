def horner(elt: str) -> int:
    "Calcule la valeur d'un entier en suivant le schéma de Horner."

    result = 0
    for digit in elt:
        result = result * 10 + (ord(digit) - ord("0"))
    return result


print(horner("1234"))
