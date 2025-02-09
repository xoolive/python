import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 10, 100)

fig, ax = plt.subplots(3, figsize=(5, 7), constrained_layout=True)

ax[0].plot(
    x,
    np.sin(x),
    "k-",
    label="sinus",
)
ax[0].plot(
    x,
    np.cos(x),
    color="tab:blue",
    linestyle="dotted",  # explicite
    label="cosinus",
)

ax[0].set_ylim((-2, 1.5))  # ajustement des limites
ax[0].legend(loc="lower left", ncol=2, prop={"family": "Ubuntu", "size": 14})

ax[1].scatter(
    np.cos(x),
    np.sin(x),
    marker=".",
    s=20,
    color="crimson",  # nom de couleur HTML
)
ax[1].set_aspect("equal")

ax[2].hist(
    np.cos(x),
    range=(-1, 1),
    bins=16,
    linewidth=2,
    color="#008f6b",  # code hexadécimal de la couleur
    edgecolor="white",
)

for ax_ in ax.ravel():
    for tick in ax_.xaxis.get_major_ticks() + ax_.yaxis.get_major_ticks():
        tick.label.set_fontsize(14)
        tick.label.set_fontname("Ubuntu")

fig.savefig("fig10.png", bbox_inches="tight")
plt.show()