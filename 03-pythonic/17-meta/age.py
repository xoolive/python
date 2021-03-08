import time

import pandas as pd


class Age:
    def __get__(self, obj, objtype=None):
        # Renvoie la durée depuis l'attribut time
        return pd.Timestamp("now") - obj.time


class Individu:

    age = Age()  # Renvoie la durée depuis la création de l'instance

    def __init__(self):
        # L'attribut time est créé lors de la création de l'instance
        self.time = pd.Timestamp("now")


i = Individu()
print(f"{i.age = }")
time.sleep(1)
print(f"{i.age = }")
