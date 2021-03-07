import time


def logger(fonction):
    def fonction_modifiee(*args):
        print(f"Exécution de la fonction {fonction.__name__}: {args}")
        resultat = fonction(*args)
        print("Terminé!")
        return resultat

    return fonction_modifiee


@logger
def pause(secondes: int = 1) -> None:
    time.sleep(secondes)
    return


pause(1)
