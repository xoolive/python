import logging
from abc import ABC, abstractmethod

import pandas as pd


class Validator(ABC):
    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = "_" + name

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        self.validate(value)
        setattr(obj, self.private_name, value)

    @abstractmethod
    def validate(self, value):
        pass


class String(Validator):
    def __init__(self, **kwargs):
        self.kwargs = kwargs

    def validate(self, value):
        for key, vrai_faux in self.kwargs.items():
            # getattr() récupère la méthode (bound method)
            # Les parenthèses suivantes () appellent la méthode. cf. __call__()
            if not getattr(value, key)() is vrai_faux:
                msg = f"Le critère str.{key} n'est pas respecté pour {value}"
                raise ValueError(msg)


class OneOf(Validator):
    def __init__(self, *options):
        self.options = set(options)

    def validate(self, value):
        if value not in self.options:
            msg = f"La valeur {value} doit être comprise dans {self.options}"
            raise ValueError(msg)
            from datetime import datetime


class AgeMin(Validator):
    def __init__(self, value=None):
        self.age_min = pd.Timedelta(value)

    def validate(self, value):
        msg = "{date} doit être antérieur à {reference:%Y}"
        reference = pd.Timestamp("now") - self.age_min
        if pd.Timestamp(value) > reference:
            raise ValueError(msg.format(date=value, reference=reference))


class PersonneMajeure:

    nom = String(istitle=True)
    genre = OneOf("M", "F")
    date_naissance = AgeMin("18y")

    def __init__(self, nom, genre, date_naissance):
        self.nom = nom
        self.genre = genre
        self.date_naissance = date_naissance

    def __repr__(self):
        return repr(vars(self))


try:
    PersonneMajeure("Nicolas", "M", "1980-11-11")
except Exception as exc:
    logging.warning(exc)
try:
    PersonneMajeure("nicolas", "M", "1980-11-11")
except Exception as exc:
    logging.warning(exc)
try:
    PersonneMajeure("Nicolas", "U", "1980-11-11")
except Exception as exc:
    logging.warning(exc)
try:
    PersonneMajeure("Nicolas", "M", "2020-11-11")
except Exception as exc:
    logging.warning(exc)
