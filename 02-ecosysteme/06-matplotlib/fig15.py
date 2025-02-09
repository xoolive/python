from datetime import datetime

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

births = pd.read_csv("../../data/births.csv")

quartiles = np.percentile(births["births"], [25, 50, 75])
mu, sig = quartiles[1], 0.74 * (quartiles[2] - quartiles[0])
births = births.query("(births > @mu - 5 * @sig) & (births < @mu + 5 * @sig)")

births["day"] = births["day"].astype(int)

births.index = pd.to_datetime(
    10000 * births.year + 100 * births.month + births.day, format="%Y%m%d"
)
births_by_date = births.pivot_table(
    "births", [births.index.month, births.index.day]
)
births_by_date.index = [
    datetime(1988, month, day) for (month, day) in births_by_date.index
]


df = births_by_date.reset_index()

fig, ax = plt.subplots(figsize=(8, 3.5))


ax.plot(df["index"], df.births, alpha=0.5)
ax.tick_params(labelsize=14, pad=10)

ax.xaxis.set_major_locator(mpl.dates.MonthLocator())
ax.xaxis.set_minor_locator(mpl.dates.WeekdayLocator(byweekday=1))
ax.xaxis.set_major_formatter(mpl.dates.DateFormatter("%h"))
ax.xaxis.set_minor_formatter(plt.NullFormatter())

ax.yaxis.set_major_locator(plt.MultipleLocator(200))

ax.grid(alpha=0.5)

ax.tick_params(axis="x", direction="in", length=7, width=1.5)
ax.tick_params(axis="x", which="minor", length=5)
ax.tick_params(axis="y", which="major", length=5)

ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

ax.plot(
    1, 0, marker=">", ms=8, color="k", transform=ax.transAxes, clip_on=False
)
ax.plot(
    0, 1, marker="^", ms=8, color="k", transform=ax.transAxes, clip_on=False
)
ax.spines["bottom"].set_linewidth(1.5)
ax.spines["left"].set_linewidth(1.5)

# Add labels to the plot
style = dict(
    size=14,
    color="tab:blue",
    va="center",
    fontname="Ubuntu",
    zorder=5,
    bbox=dict(facecolor="w", edgecolor="none"),
)


ax.text(
    datetime(1988, 1, 1),
    4400,
    "< ax.text(datetime(1988, 1, 1), 4400, txt)",
    **style,
    transform=ax.transData,
)
ax.text(
    0.1,
    0.2,
    "< ax.text(0.1, 0.2, txt, transform=ax.transAxes)",
    **style,
    transform=ax.transAxes,
)
ax.text(
    0.1,
    0.2,
    "< ax.text(0.1, 0.2, txt, transform=fig.transFigure)",
    **style,
    transform=fig.transFigure,
)

fig.savefig("fig15_1.png", bbox_inches="tight")
plt.show()

fig, ax = plt.subplots(figsize=(8, 3.5))


ax.plot(df["index"], df.births)
ax.tick_params(labelsize=14, pad=10)

ax.xaxis.set_major_locator(mpl.dates.MonthLocator())
ax.xaxis.set_minor_locator(mpl.dates.WeekdayLocator(byweekday=1))
ax.xaxis.set_major_formatter(mpl.dates.DateFormatter("%h"))
ax.xaxis.set_minor_formatter(plt.NullFormatter())

ax.yaxis.set_major_locator(plt.MultipleLocator(200))

ax.grid(alpha=0.5)

ax.tick_params(axis="x", direction="in", length=7, width=1.5)
ax.tick_params(axis="x", which="minor", length=5)
ax.tick_params(axis="y", which="major", length=5)

ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)

ax.plot(
    1, 0, marker=">", ms=8, color="k", transform=ax.transAxes, clip_on=False
)
ax.plot(
    0, 1, marker="^", ms=8, color="k", transform=ax.transAxes, clip_on=False
)
ax.spines["bottom"].set_linewidth(1.5)
ax.spines["left"].set_linewidth(1.5)

style = dict(
    size=14,
    color="tab:blue",  # couleur
    arrowprops=dict(arrowstyle="->", color="tab:blue"),  # flèche
    textcoords="offset points",
    bbox=dict(boxstyle="round", fc="white", ec="tab:blue", pad=0.5),
)

ax.annotate(
    "Jour de l'an",
    xy=(datetime(1988, 1, 1), 4009),
    xytext=(25, 0),
    ha="left",
    **style,
)
ax.annotate(
    "Jour de l'indépendance",
    xy=(datetime(1988, 7, 4), 4335),  # coordonnées du point
    xytext=(-30, 0),  # relatives au point
    ha="right",  # alignement
    **style,
)

ax.annotate(
    "Thanksgiving",
    xy=(datetime(1988, 11, 25), 4649),
    xytext=(-40, -20),
    ha="right",
    **style,
)
ax.annotate(
    "Noël",
    xy=(datetime(1988, 12, 25), 3844),
    xytext=(-30, 12),
    ha="right",
    **style,
)

ax.set_ylabel(
    "Nombre de naissances  par jour",
    fontname="Ubuntu",
    fontsize=14,
    rotation=0,
    ha="left",
)
ax.yaxis.set_label_coords(-0.12, 1.02)

fig.savefig("fig15_2.png", bbox_inches="tight")
plt.show()