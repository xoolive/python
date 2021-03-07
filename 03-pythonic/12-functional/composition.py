from functools import reduce

add_1 = lambda x: x + 1
mul_2 = lambda x: x * 2

fonctions: "list[int -> int]" = [add_1, mul_2, add_1, add_1, mul_2]


def compose(f: "int -> int", g: "int -> int") -> "int -> int":
    def f_puis_g(x):
        return g(f(x))

    return f_puis_g


full_set_of_operations: "int -> int" = reduce(compose, fonctions)
print(full_set_of_operations(3))  # ((((3 + 1) * 2) + 1) + 1) * 2


# L'application suivante est équivalente (et plus lisible)


def apply_function(x: int, f: "int -> int") -> int:
    return f(x)


print(reduce(apply_function, fonctions, 3))  # 20
