from typing import Optional


class Maybe:
    def maybe_none(self, x: int) -> Optional[int]:
        if x > 0:
            return x
        # return None


def fonction(a: Maybe, x: int = 1) -> int:
    return a.maybe_none(x) + 1
