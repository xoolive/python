import functools


def add_1(it):
    for elt in it:
        yield elt + 1


def mul_2(it):
    for elt in it:
        yield 2 * elt


chaine = functools.reduce(
    lambda x, f: f(x), [mul_2, add_1, add_1, mul_2, add_1], range(10)  # ③
)

print(f"Avec des générateurs: [mul_2, add_1, add_1, mul_2, add_1]\n    {list(chaine)}")


def coroutine(fun):
    @functools.wraps(fun)
    def wraps(*args, **kwargs):
        gen = fun(*args, **kwargs)
        next(gen)  # ①
        return gen

    return wraps


@coroutine
def add_1(output):
    while True:
        elt = yield
        output.send(elt + 1)


@coroutine
def mul_2(output):
    while True:
        elt = yield
        output.send(elt * 2)


@coroutine
def ajoute(liste):
    while True:
        elt = yield
        liste.append(elt)


resultat = list()
chaine = functools.reduce(
    lambda x, f: f(x),
    [add_1, mul_2, add_1, add_1, mul_2],  # ④
    ajoute(resultat),
)

for elt in range(10):
    chaine.send(elt)

print(f"Avec des coroutines: [add_1, mul_2, add_1, add_1, mul_2]\n    {resultat}")