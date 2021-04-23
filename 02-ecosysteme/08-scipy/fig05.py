import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.stats import expon, gumbel_r

# https://data.toulouse-metropole.fr/explore/dataset/27-station-meteo-toulouse-saint-cyprien/export/
df = pd.read_csv(
    "../../data/27-station-meteo-toulouse-saint-cyprien.csv",
    sep=";",
    parse_dates=["heure_utc"],
    usecols=[
        "heure_utc",
        "temperature",
        "pression",
        "humidite",
        "force_moyenne_du_vecteur_de_vent",
    ],
)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))

vent = df.force_moyenne_du_vecteur_de_vent
y, x, _ = ax1.hist(
    x=vent,
    bins=16,
    lw=2,
    ec="white",
    fc="black",
    density=True,
    # label="force du vent (km/h)",
)

x_ = np.linspace(x[0], x[-1], 100)
ax1.plot(x_, expon.pdf(x_, scale=vent.mean()), color="white", lw=10)
ax1.plot(
    x_,
    expon.pdf(x_, scale=vent.mean()),
    color="tab:red",
    lw=3,
    label="scipy.stats.expon.pdf()",
)

ax1.legend(
    prop={
        "family": "Ubuntu",
        "size": 14,
    },
    borderpad=0.5,
)

vent_max = (
    df.assign(day=lambda df: df.heure_utc.dt.round("1d"))
    .groupby("day")
    .agg(dict(force_moyenne_du_vecteur_de_vent="max"))
    .force_moyenne_du_vecteur_de_vent
)

y, x, _ = ax2.hist(
    x=vent_max,
    bins=16,
    lw=2,
    ec="white",
    fc="black",
    density=True,
    # label="force du vent (km/h)",
)
(loc, scale), _ = curve_fit(
    lambda x, loc, scale: gumbel_r.pdf(x, loc=loc, scale=scale),
    (x[:-1] + x[1:]) / 2,
    y,
)

ax2.plot(x_, gumbel_r.pdf(x_, loc=loc, scale=scale), color="white", lw=10)
ax2.plot(
    x_,
    gumbel_r.pdf(x_, loc=loc, scale=scale),
    color="tab:red",
    lw=3,
    label="scipy.stats.gumbel_r.pdf()",
)

ax2.legend(
    prop={
        "family": "Ubuntu",
        "size": 14,
    },
    borderpad=0.5,
)
style = dict(fontfamily="Ubuntu", size=16, pad=25)
ax1.set_title("Mesures moyennes de la force du vent", **style)
ax2.set_title("Mesures maximales de la force du vent par jour", **style)

for ax_ in [ax1, ax2]:
    for tick in ax_.xaxis.get_major_ticks() + ax_.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)
        tick.label.set_fontname("Ubuntu")

    for s in ax_.spines.values():
        s.set_linewidth(1.5)
    ax_.spines["top"].set_visible(False)
    ax_.spines["right"].set_visible(False)

    ax_.set_ylabel(
        "Fréquence",
        fontname="Ubuntu",
        fontsize=14,
        rotation=0,
        ha="left",
    )
    ax_.set_xlabel(
        "Force du vent en km/h",
        fontname="Ubuntu",
        fontsize=14,
    )
    ax_.yaxis.set_label_coords(-0.12, 1.02)

fig.savefig("fig05.png", bbox_inches="tight")

plt.show()
