import functools
import time


def chronometre(fonction):
    name = fonction.__name__

    @functools.wraps(fonction)
    def chrono_fonction(*args):
        t0 = time.perf_counter()
        arg_str = ", ".join(repr(arg) for arg in args)
        result = fonction(*args)
        elapsed = time.perf_counter() - t0
        print(f"[{elapsed:0.8f}s] {name}({arg_str})")
        return result

    return chrono_fonction


@chronometre
def pause(secondes: int = 1) -> None:
    """Carpe diem!"""
    time.sleep(secondes)
    return


@chronometre
def factorielle(n: int) -> int:
    """Renvoie la factorielle calculée par récursion."""
    if n == 0:
        return 1
    return n * factorielle(n - 1)


pause()
factorielle(6)
