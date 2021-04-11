class Polygone:
    def aire(self) -> float:
        raise NotImplementedError

    def simplify(self) -> "Polygone":
        raise NotImplementedError

    def __lt__(self, other: "Polygone") -> bool:
        return self.aire() < other.aire()

    def __repr__(self) -> str:
        return f"Polygone d’aire {self.aire():.2f}"


class Triangle(Polygone):
    def __init__(self, p1: complex, p2: complex, p3: complex):
        self.v1 = p2 - p1
        self.v2 = p3 - p1

    def aire(self) -> float:
        return abs((self.v1.conjugate() * self.v2).imag) / 2.0

    def simplify(self) -> "Triangle":
        return self

    def __lt__(self, other: "Polygone") -> bool:
        return self.aire() < other.aire()
