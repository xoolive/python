class Distance:
    unit = "m"
    unites_derivees = dict()
    value: float

    # abrégé

    @classmethod
    def __init_subclass__(cls):
        super().__init_subclass__()
        Distance.unites_derivees[cls.unit] = cls


class Distance_ft(Distance):
    unit = "ft"

    def convert_si(self) -> float:
        return self.value * 0.3048


class Distance_nm(Distance):
    unit = "nm"

    def convert_si(self) -> float:
        return self.value * 1852


print(f"{Distance.unites_derivees = }")
