def fact_iter(n: int, cumul: int = 1) -> "Iterator[int]":
    if n == 0:  # nécessaire pour interrompre la récursion
        return
    yield cumul
    yield from fact_iter(n - 1, n * cumul)


print(f"Résultats intermédiaires: {list(fact_iter(6))}")
*_, result = fact_iter(6)
print(f"Résultat final: *_, result = fact_iter(6)")
print(f"{result = }")