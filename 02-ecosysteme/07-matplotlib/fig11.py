import matplotlib.colors as mcolors
import matplotlib.pyplot as plt


def plot_colortable(colors, title, sort_colors=True, emptycols=0):

    cell_width = 212
    cell_height = 22
    swatch_width = 48
    margin = 14
    topmargin = 40

    # Sort colors by hue, saturation, value and name.
    if sort_colors is True:
        by_hsv = sorted(
            (tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(color))), name)
            for name, color in colors.items()
        )
        names = [name for hsv, name in by_hsv]
    else:
        names = list(colors)

    n = len(names)
    ncols = 4 - emptycols
    nrows = n // ncols + int(n % ncols > 0)

    width = cell_width * 4 + 2 * margin
    height = cell_height * nrows + margin + topmargin
    dpi = 72

    fig, ax = plt.subplots(figsize=(width / dpi, height / dpi), dpi=dpi)
    fig.subplots_adjust(
        margin / width,
        margin / height,
        (width - margin) / width,
        (height - topmargin) / height,
    )
    ax.set_xlim(0, cell_width * 4)
    ax.set_ylim(cell_height * (nrows - 0.5), -cell_height / 2.0)
    ax.yaxis.set_visible(False)
    ax.xaxis.set_visible(False)
    ax.set_axis_off()
    ax.set_title(title, fontsize=24, loc="left", pad=10)

    for i, name in enumerate(names):
        row = i % nrows
        col = i // nrows
        y = row * cell_height

        swatch_start_x = cell_width * col
        swatch_end_x = cell_width * col + swatch_width
        text_pos_x = cell_width * col + swatch_width + 7

        ax.text(
            text_pos_x,
            y,
            name,
            fontname="Ubuntu",
            fontsize=16,
            horizontalalignment="left",
            verticalalignment="center",
        )

        ax.hlines(
            y, swatch_start_x, swatch_end_x, color=colors[name], linewidth=18
        )

    for col, title in enumerate(
        [
            "Couleurs de base",
            "Palette par défaut",
            "Couleurs XKCD",
            "Couleurs HTML",
        ]
    ):
        ax.text(
            col * 0.25 + 0.01,
            1.1,
            title,
            va="center",
            ha="left",
            fontname="Ubuntu",
            fontsize=16,
            transform=ax.transAxes,
        )

    return fig


colors = {
    **{
        "b": (0, 0, 1),
        "g": (0, 0.5, 0),
        "r": (1, 0, 0),
        "c": (0, 0.75, 0.75),
        "m": (0.75, 0, 0.75),
        "y": (0.75, 0.75, 0),
        "k": (0, 0, 0),
    },
    **{
        "tab:blue": "#1f77b4",
        "tab:orange": "#ff7f0e",
        "tab:green": "#2ca02c",
        "tab:red": "#d62728",
        "tab:purple": "#9467bd",
        "tab:brown": "#8c564b",
        "tab:pink": "#e377c2",
    },
    **dict(
        ("xkcd:" + c, mcolors.XKCD_COLORS["xkcd:" + c])
        for c in [
            "dull blue",
            "deep orange",
            "emerald",
            "cherry",
            "sand yellow",
            "light purple",
            "baby poop",
        ]
    ),
    **dict(
        (c, mcolors.CSS4_COLORS[c])
        for c in [
            "navy",
            "crimson",
            "limegreen",
            "darkorange",
            "gold",
            "lightseagreen",
            "purple",
        ]
    ),
}

fig = plot_colortable(
    colors,
    sort_colors=False,
    title="",
)
fig.savefig("fig11.png", bbox_inches="tight")

plt.show()