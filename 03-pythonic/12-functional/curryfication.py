from functools import partial


def add(x: float, y: float) -> float:
    return x + y


def add_curry(x: float) -> "float -> float":
    def add_x(y: float) -> float:
        return x + y

    return add_x


# Les trois notations suivantes sont équivalentes

print(add_curry(1)(2))

add_1 = add_curry(1)
print(add_1(2))

add_1 = partial(add, 1)
print(add_1(2))
