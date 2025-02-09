import matplotlib.pyplot as plt
import numpy as np

cmaps = [
    (
        "Tables qualitatives",
        ["Pastel1", "Set2", "Paired", "tab10", "tab20"],
    ),
    (
        "Tables séquentielles",
        ["Greys", "Blues", "Reds", "YlOrRd", "OrRd", "YlGn"],
    ),
    (
        "Tables divergentes",
        ["PiYG", "RdBu", "Spectral"],
    ),
    (
        "Autres tables",
        ["viridis", "terrain", "cubehelix"],
    ),
]


gradient = np.linspace(0, 1, 256)
gradient = np.vstack((gradient, gradient))


def plot_color_gradients(cmap_category, cmap_list):
    # Create figure and adjust figure height to number of colormaps
    nrows = len(cmap_list)
    figh = 0.35 + 0.15 + (nrows + (nrows - 1) * 0.1) * 0.22
    fig, axs = plt.subplots(nrows=nrows, figsize=(6.4, figh))
    fig.subplots_adjust(
        top=1 - 0.25 / figh, bottom=0.1 / figh, left=0.2, right=0.99
    )

    axs[0].set_title(cmap_category, fontname="Ubuntu", fontsize=20, pad=10)

    for ax, name in zip(axs, cmap_list):
        ax.imshow(gradient, aspect="auto", cmap=plt.get_cmap(name))
        ax.text(
            -0.25,
            0.5,
            name,
            va="center",
            ha="left",
            fontname="Ubuntu",
            fontsize=16,
            transform=ax.transAxes,
        )

    # Turn off *all* ticks & spines, not just the ones with colormaps.
    for ax in axs:
        ax.set_axis_off()

    return fig


for i, (cmap_category, cmap_list) in enumerate(cmaps):
    f = plot_color_gradients(cmap_category, cmap_list)
    f.savefig(f"fig12_{i}.png", bbox_inches="tight")
    plt.show()
