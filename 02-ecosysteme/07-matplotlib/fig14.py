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
    pd.datetime(1988, month, day) for (month, day) in births_by_date.index
]


df = births_by_date.reset_index()

fig, ax = plt.subplots(3, 1, figsize=(8, 7))
fig.subplots_adjust(hspace=0.4)


for ax_ in ax:  # ①
    ax_.plot(df["index"], df.births)
    ax_.yaxis.set_major_locator(plt.MultipleLocator(500))

    ax_.tick_params(labelsize=14, pad=10)

for ax_ in ax[1:]:  #  ②
    ax_.xaxis.set_major_locator(mpl.dates.MonthLocator())
    ax_.xaxis.set_minor_locator(mpl.dates.WeekdayLocator())
    ax_.xaxis.set_major_formatter(mpl.dates.DateFormatter("%h"))
    ax_.xaxis.set_minor_formatter(plt.NullFormatter())

    ax_.tick_params(axis="x", direction="in", length=7, width=1.5)
    ax_.tick_params(axis="x", which="minor", length=5)
    ax_.tick_params(axis="y", which="major", length=5)

for ax_ in ax[2:]:
    # ③
    ax_.spines["right"].set_visible(False)
    ax_.spines["top"].set_visible(False)
    ax_.spines["bottom"].set_linewidth(1.5)
    ax_.spines["left"].set_linewidth(1.5)

    # ④
    ax_.grid(alpha=0.5, which="major")

    style = dict(ms=8, color="k", transform=ax_.transAxes, clip_on=False)
    ax_.plot(1, 0, marker=">", **style)
    ax_.plot(0, 1, marker="^", **style)

ax[0].text(
    -0.01,
    0.8,
    "①",
    fontsize=24,
    ha="right",
    color="crimson",
    transform=ax[0].transAxes,
)
ax[1].text(
    0.05,
    0.05,
    "②",
    fontsize=24,
    ha="left",
    color="crimson",
    transform=ax[1].transAxes,
)

ax[2].text(
    1,
    1,
    "③",
    fontsize=24,
    ha="center",
    va="center",
    color="crimson",
    transform=ax[2].transAxes,
)

ax[2].text(
    datetime(1988, 9, 1),
    4500,
    "④",
    fontsize=24,
    ha="center",
    va="center",
    color="crimson",
)

fig.savefig("fig14.png", bbox_inches="tight")
plt.show()
