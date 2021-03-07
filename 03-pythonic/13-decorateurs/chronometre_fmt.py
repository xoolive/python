import time

DEFAULT_FMT = "[{elapsed:0.8f}s] {name}({args}) -> {result}"


def chronometre_fmt(fmt=DEFAULT_FMT):
    def decorateur(func):
        def chrono_fonction(*_args):
            t0 = time.time()
            result = func(*_args)
            elapsed = time.time() - t0
            name = func.__name__
            args = ", ".join(repr(arg) for arg in _args)
            print(fmt.format(**locals()))
            return result

        return chrono_fonction

    return decorateur


@chronometre_fmt()
def pause(seconds):
    time.sleep(seconds)


for i in range(3):
    pause(0.123)
