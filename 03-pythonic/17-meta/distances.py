from typing import Dict, List, Type, TypedDict


class DistanceDict(TypedDict):
    value: int
    unit: str
    conversion: float


distances: List[DistanceDict] = [
    {"value": 2, "unit": "m"},  # type: ignore
    {"value": 6, "unit": "ft", "conversion": 0.3048},
    {"value": 3, "unit": "km", "conversion": 1000},
    {"value": 1, "unit": "nm", "conversion": 1852},
]


class Distance:
    "La classe de base dont hériteront toutes les unités."

    unit = "m"

    def __init__(self, value: float):
        self.value = value

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.value}) = {self.convert_si():.2f}m"

    def __lt__(self, other):
        return self.convert_si() < other.convert_si()

    def convert_si(self) -> float:
        return self.value


classes: Dict[str, Type[Distance]] = {"m": Distance}
instances = list()

for elt in distances:
    unit = elt["unit"]
    cls = classes.get(unit, None)

    if cls is None:  # si la classe n'existe pas encore, on la génère

        def convert_si(elt):
            return lambda self: self.value * elt["conversion"]

        # Création de deux attributs supplémentaires
        attr_dict = dict(unit=unit, convert_si=convert_si(elt))
        # Création de la classe avec le mot-clé type
        cls = classes[unit] = type(f"Distance_{unit}", (Distance,), attr_dict)

    # Instantiation de la classe
    instances.append(cls(elt["value"]))


print(f"{sorted(instances) = }")
print(f"{classes = }")
