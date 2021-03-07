from typing import List


def fibonacci(n: int) -> int:
    """Renvoie la n-e valeur de la suite de Fibonacci"""
    if n in [0, 1]:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


def n_premiers(function: "int -> int", n: int) -> List[int]:
    """Renvoie la liste des n premiers éléments de la suite de Fibonacci."""
    return [function(i) for i in range(n)]


def premiers(function: "int -> int") -> "int -> List[int]":
    """Renvoie une fonction qui renvoie les n premiers éléments."""

    def n_premiers_fun(n: "int") -> List[int]:
        return n_premiers(function, n)

    return n_premiers_fun


n_premiers_fibonacci = premiers(fibonacci)
print(n_premiers_fibonacci(8))
