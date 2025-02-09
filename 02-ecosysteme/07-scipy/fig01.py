import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import interp1d

np.random.seed(150)

x_data = np.linspace(0, 3, num=21)
y_data = 3 * np.sin(x_data ** 2)  # + np.random.normal(size=20)

fig, ax = plt.subplots(figsize=(7, 5))

ax_in = ax.inset_axes([0.37, 0.3, 0.35, 0.45])

x_new = np.linspace(0, 3, num=121)

for ax_ in [ax, ax_in]:
    # ax_.scatter(x_data, y_data, s=50, color="w", zorder=3)
    ax_.scatter(x_data, y_data, zorder=4, s=70, edgecolor="w", lw=2)

    f_l = interp1d(x_data, y_data)
    l_ = ax_.plot(x_new, f_l(x_new), "C1:", lw="3", label="linear")

    f_n = interp1d(x_data, y_data, kind="nearest")
    n_ = ax_.plot(x_new, f_n(x_new), "C2--", label="nearest")

    f_c = interp1d(x_data, y_data, kind="cubic")
    c_ = ax_.plot(x_new, f_c(x_new), "C3", label="cubic")

ax_in.set_xlim((2.6, 3))
ax_in.set_ylim((2.2, 3.1))
ax_in.xaxis.set_major_locator(plt.NullLocator())
ax_in.yaxis.set_major_locator(plt.NullLocator())
for s in ax_in.spines.values():
    s.set_linewidth(2)

ax.indicate_inset_zoom(ax_in, lw=2)

for ax_ in [ax]:

    for s in ax_.spines.values():
        s.set_linewidth(1.5)

    ax_.spines["top"].set_visible(False)
    ax_.spines["right"].set_visible(False)
    ax_.spines["left"].set_position("zero")
    ax_.spines["bottom"].set_position("zero")

    ax.xaxis.set_major_locator(plt.FixedLocator([1, 2, 3]))

    for tick in ax_.xaxis.get_major_ticks() + ax_.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)
        tick.label.set_fontname("Ubuntu")

ax.legend(
    sum([l_, n_, c_], []),
    ['kind="linear"', 'kind="nearest"', 'kind="cubic"'],
    loc=(0.1, 0),
    prop={
        "family": "Ubuntu",
        "size": 15,
    },
    borderpad=0.5,
)

fig.savefig("fig01.png", bbox_inches="tight")

plt.show()
