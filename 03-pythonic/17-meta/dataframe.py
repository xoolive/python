import pandas as pd

tours = {
    "nom": ["Tour Eiffel", "Torre de Belém", "London Tower"],
    "ville": ["Paris", "Lisboa", "London"],
    "latitude": [48.85826, 38.6916, 51.508056],
    "longitude": [2.2945, -9.216, -0.076111],
    "hauteur": [324, 30, 27],
}


class DataFrameWrapper:
    def __new__(cls, data: pd.DataFrame):
        if data.shape[0] > 0:  # ②
            return super().__new__(cls)
        return None

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data

    def __repr__(self):
        return f"Tableau à {self.data.shape[0]} lignes"

    def query(self, *args, **kwargs):
        return type(self)(self.data.query(*args, **kwargs))


w = DataFrameWrapper(pd.DataFrame.from_dict(tours))
print(f"{w.query('hauteur > 300') = }")
print(f"{w.query('hauteur > 1000') = }")
