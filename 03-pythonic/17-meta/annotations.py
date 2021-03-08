import logging
from abc import ABC, abstractmethod


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


class VariableVerifier(Validator):
    def __init__(self, annotation):
        self.annotation = annotation

    def validate(self, value):
        if not isinstance(value, self.annotation):
            raise TypeError(f"{self.public_name} doit être de type: {self.annotation}")


class ValidateAnnotationsMeta(type):
    def __new__(cls, name, bases, attr_dict):  # ②

        if annotations := attr_dict.get("__annotations__"):
            for key, value in annotations.items():
                # value est ici le type passé dans l'annotation
                attr_dict[key] = VariableVerifier(value)  # ③

        return super().__new__(cls, name, bases, attr_dict)  # ④


class Exemple(metaclass=ValidateAnnotationsMeta):  # ⑤

    x: int

    def __init__(self, x):
        self.x = x

    def __repr__(self):
        return f"{type(self).__name__}({self.x})"


class Exemple_xy(Exemple):
    # Comme Exemple_xy hérite de Exemple, la classe sera créée à l'aide de la
    # méthode __new__ de la métaclasse ValidateAnnotationsMeta.
    # Le descripteur associé à x sera réalisé à la création de la classe Exemple;
    # celui associé à y sera réalisé lors d'un autre appel à la création de Exemple_xy.

    y: str

    def __init__(self, x, y):
        super().__init__(x)
        self.y = y

    def __repr__(self):
        return f"{type(self).__name__}({self.x}, {self.y})"


try:
    print(f"{Exemple_xy(3, 2) = }")
except Exception as exc:
    logging.warning(exc)
try:
    print(f"{Exemple_xy(3, '2')}")
except Exception as exc:
    logging.warning(exc)
