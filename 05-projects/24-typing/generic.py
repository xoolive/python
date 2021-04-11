from typing import Any, Callable, Generic, TypeVar
import functools

T = TypeVar("T", int, str)


class prefixe(Generic[T]):
    def __init__(self, elt: T) -> None:
        self.elt: T = elt

    def __call__(self, fun: Callable[..., T]) -> Callable[..., T]:
        @functools.wraps(fun)
        def newfun(*args: Any, **kwargs: Any) -> T:
            return self.elt + fun(*args, **kwargs)

        return newfun


@prefixe(">>> ")
def resultat_1() -> str:
    return "un"


@prefixe(2)
def resultat_2() -> int:
    return 2


@prefixe(">>> ")
def resultat_3() -> int:
    return 3


reveal_type(prefixe(">>>"))
reveal_type(prefixe(2))


@prefixe(2.4)
def resultat_4() -> float:
    return 4