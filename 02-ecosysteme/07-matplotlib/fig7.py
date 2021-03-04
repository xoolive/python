import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(7, 7))

ax = np.array(
    [
        [fig.add_subplot(221), fig.add_subplot(222)],
        [fig.add_subplot(223), fig.add_subplot(224, projection="3d")],
    ]
)

title_style = dict(pad=10, fontname="Ubuntu", fontsize=18)

x, y = np.meshgrid(np.linspace(0, 5, 100), np.linspace(0, 5, 100))
z = np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)

img = ax[0, 0].pcolormesh(x, y, z, shading="auto")
ax[0, 0].set_title("ax.pcolormesh(z)", **title_style)
ax[0, 0].set_aspect(1)

ax[0, 1].contour(x, y, z)
ax[0, 1].set_title("ax.contour(z)", **title_style)
ax[0, 1].set_aspect(1)

dx = (
    -10 * np.cos(x) * np.sin(x) ** 9
    - y * np.sin(10 + y * x) * np.cos(x)
    - np.cos(10 + y * x) * np.sin(x)
)
dy = -np.cos(x) * x * np.sin(10 + y * x)
step = 8
ax[1, 0].quiver(
    x[::step, ::step],
    y[::step, ::step],
    dx[::step, ::step],
    dy[::step, ::step],
    pivot="mid",
    units="inches",
    width=0.017,
)
ax[1, 0].set_title("ax.quiver(x, y, dx, dy)", **title_style)
ax[1, 0].set_aspect(1)

ax[1, 1].plot_surface(x, y, z, cmap="viridis", linewidth=0, antialiased=False)
ax[1, 1].set_title("ax.plot_surface(x, y, z)", **title_style)
ax[1, 1].view_init(elev=30.0, azim=290)


for ax_ in ax.ravel():
    for tick in ax_.xaxis.get_major_ticks() + ax_.yaxis.get_major_ticks():
        tick.label.set_fontsize(14)
        tick.label.set_fontname("Ubuntu")

fig.subplots_adjust(hspace=0.3, wspace=0.1)

cax = plt.axes([0.95, 0.2, 0.04, 0.6])
cbar = fig.colorbar(img, cax=cax)

for tick in cbar.ax.get_ymajorticklabels():
    tick.set_fontsize(14)
    tick.set_fontname("Ubuntu")

fig.savefig("fig7.png", bbox_inches="tight")

plt.show()
