import functools
from itertools import count


def coroutine(fun):
    @functools.wraps(fun)
    def wraps(*args, **kwargs):
        gen = fun(*args, **kwargs)
        next(gen)  # ①
        return gen

    return wraps


@coroutine
def moyenne():
    total = 0.0
    average = None
    for compteur in count(1):  # ②
        terme = yield average
        total += terme
        average = total / compteur


sequence = [2, 3, 7, 6, 4, 5, 8, 9, 1]
moy = moyenne()

print(f"{sequence = }")
print(", ".join(f"{elt} -> {moy.send(elt)}" for elt in sequence))
print("On continue...")
print(", ".join(f"{elt} -> {moy.send(elt):.2f}" for elt in sequence))
