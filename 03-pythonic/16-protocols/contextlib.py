import contextlib


@contextlib.contextmanager
def dangereux():
    print("\033[1;31m", end="")
    try:
        yield "ROUGE!"
    except ZeroDivisionError:
        print("NE PAS diviser par zéro !!")
    else:
        print("\033[1;34mOK")
    finally:
        print("\033[0m", end="")


with dangereux():
    print(1 / 2)
with dangereux():
    print(1 / 0)
with dangereux() as color:
    print(color)
    b = a
