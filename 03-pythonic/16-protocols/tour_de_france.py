from typing import Iterator

import matplotlib.pyplot as plt
import pandas as pd
from cartes.crs import Lambert93, PlateCarree

df = pd.read_csv("./data/tour_de_france.csv.gz", parse_dates=["timestamp"])


class Trajectoire:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    @property
    def start(self) -> pd.Timestamp:
        return self.data.timestamp.min()

    @property
    def stop(self) -> pd.Timestamp:
        return self.data.timestamp.max()

    @property
    def duree(self) -> pd.Timedelta:
        return self.stop - self.start

    def plot(self, ax, **kwargs):
        return self.data.plot(
            ax=ax,
            x="longitude",
            y="latitude",
            legend=False,
            transform=PlateCarree(),
            **kwargs,
        )


class Collection:
    def __init__(self, data: pd.DataFrame):
        self.data = data

    def __iter__(self) -> Iterator[Trajectoire]:  # ④
        df = self.data.sort_values("timestamp").assign(
            timestamp_diff=lambda df: df.timestamp.diff().dt.total_seconds()
        )
        seuil = df.query("timestamp_diff > 3600")

        if seuil.shape[0] == 0:
            return Trajectoire(self.data)
        else:
            yield Trajectoire(df.query("timestamp < @seuil.timestamp.min()"))
            yield from Collection(df.query("timestamp >= @seuil.timestamp.min()"))

    def __len__(self):
        return sum(1 for _ in self)


fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(projection=Lambert93()))

ax.coastlines("50m")

for i, trajectoire in enumerate(Collection(df)):
    trajectoire.plot(ax=ax, color="#b45118")
    dernier = trajectoire.data.iloc[-1]
    ax.text(
        x=dernier.longitude,
        y=dernier.latitude,
        s=f"{trajectoire.start:%b %d}",
        transform=PlateCarree(),
        fontname="Ubuntu",
        fontsize=14,
        ha="right" if i % 2 else "left",
    )

ax.set_extent((-4, 8, 42, 51))
ax.set_yticks([])
ax.spines["geo"].set_visible(False)

fig.savefig("tour_de_france.png")
plt.show()

# Code supplémentaire pour affichage du résultat dans le terminal

import locale

from rich.console import Console
from rich.table import Table

locale.setlocale(locale.LC_ALL, "")

console = Console()
table = Table(show_header=True, header_style="bold magenta")
table.add_column("Début", justify="right")
table.add_column("Fin", justify="right")
table.add_column("Durée", justify="right")

for trajectoire in Collection(df):
    table.add_row(
        f"{trajectoire.start:%d %B %H:%M}",
        f"{trajectoire.stop:%d %B %H:%M}",
        f"{trajectoire.duree}",
    )

console.print(table)
