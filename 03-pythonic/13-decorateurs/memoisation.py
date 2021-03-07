import functools
import time


def pile_d_appel(fonction):
    name: str = fonction.__name__
    indentation: int = -1
    t0: "timestamp" = None

    @functools.wraps(fonction)
    def chrono_fonction(*args):
        nonlocal indentation, t0
        indentation += 1
        t0 = time.perf_counter() if t0 is None else t0
        arg_str = ", ".join(repr(arg) for arg in args)

        elapsed = time.perf_counter() - t0
        print(f"{' '*indentation}[{elapsed:0.8f}s] {name}({arg_str}) -> ...")
        result = fonction(*args)
        elapsed = time.perf_counter() - t0
        print(
            f"{' '*indentation}[{elapsed:0.8f}s] {name}({arg_str}) -> {result}"
        )
        indentation -= 1

        return result

    return chrono_fonction


@pile_d_appel
def fibonacci(n: int) -> int:
    """Renvoie la n-e valeur de la suite de Fibonacci"""
    if n in [0, 1]:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


print(">>> Sans mémoisation")
fibonacci(10)


@pile_d_appel
@functools.lru_cache()
def memo_fibonacci(n: int) -> int:
    """Renvoie la n-e valeur de la suite de Fibonacci"""
    if n in [0, 1]:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


print()
print(">>> Avec mémoisation")
memo_fibonacci(10)
