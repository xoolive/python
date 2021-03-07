import time


class chronometre_fmt:
    DEFAULT_FMT = "[{elapsed:0.8f}s] {name}({args}) -> {result}"

    def __init__(self, fmt: str = None):
        self.fmt = fmt if fmt is not None else self.DEFAULT_FMT

    def __call__(self, func):
        def chrono_fonction(*_args):
            t0 = time.time()
            result = func(*_args)
            elapsed = time.time() - t0
            name = func.__name__
            args = ", ".join(repr(arg) for arg in _args)
            print(self.fmt.format(**locals()))
            return result

        return chrono_fonction


@chronometre_fmt()
def pause(seconds):
    time.sleep(seconds)


for i in range(3):
    pause(0.123)
