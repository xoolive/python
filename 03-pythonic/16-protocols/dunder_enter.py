class Dangereux:
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_value, traceback):
        handled = False

        if exc_type is ZeroDivisionError:  # except ZeroDivisionError:
            print("NE PAS diviser par zéro !!")
            handled = True

        if exc_type is None:  # else:
            print("OK")
            handled = True

        # finally:
        print(f"On remballe")

        # si on renvoie True, Python considère que l'exception est rattrapée
        return handled


with Dangereux():  # cas nominal
    y = 1 / 2
with Dangereux():  # exception gérée
    y = 1 / 0
with Dangereux():  # exception non gérée
    a = b
