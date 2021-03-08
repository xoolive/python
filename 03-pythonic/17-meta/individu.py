import logging


class LoggedAccess:
    def __set_name__(self, obj, name):
        self.public_name = name
        # on va créer les attributs _nom et _age
        self.private_name = "_" + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        logging.warning(f"Mise à jour de l'attribut {self.public_name}={value}")
        setattr(obj, self.private_name, value)


class Individu:

    nom = LoggedAccess()
    age = LoggedAccess()

    def __init__(self, nom, age):
        self.nom = nom
        self.age = age

    def __repr__(self):
        return repr(vars(self))


nico = Individu("Nicolas", 39)
nico.age = 40
print(f"{nico = }")
