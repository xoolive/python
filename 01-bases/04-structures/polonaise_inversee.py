from collections import deque


def compute(sequence: list) -> int:
    d = deque()
    for touche in sequence:
        if isinstance(touche, int):
            d.append(touche)
        elif isinstance(touche, str):
            b, a = d.pop(), d.pop()
            expr = f"{a} {touche} {b}"
            d.append(eval(expr))
        else:
            raise ValueError(f"Expression invalide: {touche}")
        print(f"{d}  # {touche}")
    return d.pop()


compute([3, 1, 2, "+", 4, "*", "+"])
