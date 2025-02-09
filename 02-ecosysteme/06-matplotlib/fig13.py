import matplotlib.pyplot as plt
import numpy as np

x, y = np.meshgrid(np.linspace(0, 5, 100), np.linspace(0, 5, 100))
z = np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)

fig, ax = plt.subplots(1, 3, figsize=(15, 6), sharey=True)
fig.subplots_adjust(wspace=0)

maps = ["viridis", "YlOrRd", "RdBu"]

for i, ax_ in enumerate(ax):
    img = ax_.imshow(z, extent=[0, 5, 0, 5], origin="lower", cmap=maps[i])

    cbar = fig.colorbar(
        img,
        ax=ax_,
        orientation="horizontal",
        shrink=0.7,
        pad=0.12,
        ticks=[],
        drawedges=False,
    )
    cbar.ax.set_title(f'cmap="{maps[i]}"', fontname="Ubuntu", fontsize=18, y=-3)

    for tick in ax_.xaxis.get_major_ticks() + ax_.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)
        tick.label.set_fontname("Ubuntu")

    ax_.tick_params(pad=7)

fig.savefig("fig13.png", bbox_inches="tight")
plt.show()