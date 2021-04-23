import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata

x, y = np.meshgrid(np.linspace(0, 5, 100), np.linspace(0, 5, 100))

fig, ax = plt.subplots(2, 2, figsize=(7, 7), sharex=True, sharey=True)


def f(x, y):
    return np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)


style = dict(fontfamily="Ubuntu", size=16, pad=10)


ax[0, 0].imshow(
    f(x, y),
    extent=[0, 5, 0, 5],
    origin="lower",
)
ax[0, 0].set_title("Référence", **style)

x_, y_ = np.random.uniform(0, 5, (2, 300))

ax[0, 1].scatter(x_, y_, c=f(x_, y_), cmap="viridis")
ax[0, 1].set(xlim=(0, 5), ylim=(0, 5), aspect=1)
ax[0, 1].set_title("np.random.uniform()", **style)

ax[1, 0].imshow(
    griddata(
        np.c_[x_, y_], f(x_, y_), (x, y), fill_value="nan", method="nearest"
    ),
    extent=[0, 5, 0, 5],
    origin="lower",
)
ax[1, 0].set_title('method="nearest"', **style)
ax[1, 1].imshow(
    griddata(
        np.c_[x_, y_], f(x_, y_), (x, y), fill_value="nan", method="cubic"
    ),
    extent=[0, 5, 0, 5],
    origin="lower",
)
ax[1, 1].set_title('method="cubic"', **style)

fig.subplots_adjust(hspace=0.25)

for ax_ in ax.ravel():
    ax_.tick_params(pad=7)
    for tick in ax_.xaxis.get_major_ticks() + ax_.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)
        tick.label.set_fontname("Ubuntu")

fig.savefig("fig02.png", bbox_inches="tight")

plt.show()
