import matplotlib.pyplot as plt
import numpy as np
from matplotlib import animation
from matplotlib.patches import ConnectionPatch
from tqdm.autonotebook import tqdm


def format_func(value, tick_number):
    # find number of multiples of pi/2
    N = int(np.round(2 * value / np.pi))
    if N == 0:
        return ""
    elif N == 1:
        return r"$\pi/2$"
    elif N == 2:
        return r"$\pi$"
    elif N % 2 > 0:
        return r"${0}\pi/2$".format(N)
    else:
        return r"${0}\pi$".format(N // 2)


fig, ax = plt.subplots(
    1, 2, figsize=(10, 3), gridspec_kw=dict(width_ratios=(3, 5))
)

angle = np.linspace(0, 2 * np.pi, 200)

ax[0].set_aspect("equal")
ax[0].plot(np.cos(angle), np.sin(angle))
ax[0].spines["left"].set_position("center")
ax[0].xaxis.set_major_locator(plt.FixedLocator([-1, 1]))
ax[0].yaxis.set_major_locator(plt.FixedLocator([-1, 1]))

ax[1].plot(angle, np.sin(angle))
ax[1].spines["left"].set_position("zero")
ax[1].xaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
ax[1].yaxis.set_major_locator(plt.MultipleLocator(1))

ax[1].xaxis.set_major_formatter(plt.FuncFormatter(format_func))

for ax_ in ax:
    ax_.spines["bottom"].set_position("center")
    ax_.spines["top"].set_visible(False)
    ax_.spines["right"].set_visible(False)

    ax_.tick_params(labelsize=14, pad=10, length=7)


line1, *_ = ax[0].plot([0, np.cos(np.pi / 4)], [0, np.sin(np.pi / 4)], "-o")
line2, *_ = ax[1].plot([np.pi / 4, np.pi / 4], [0, np.sin(np.pi / 4)], "-o")


con = ConnectionPatch(
    xyA=(np.pi / 4, np.sin(np.pi / 4)),
    xyB=(np.cos(np.pi / 4), np.sin(np.pi / 4)),
    coordsA="data",
    coordsB="data",
    axesA=ax[1],
    axesB=ax[0],
    color="tab:orange",
    lw=1.5,
)
ax[1].add_artist(con)


def set_angle(angle, line1, line2):
    global con
    line1.set_data([0, np.cos(angle)], [0, np.sin(angle)])
    line2.set_data([angle, angle], [0, np.sin(angle)])
    # particularité: le ConnectionPatch ne peut être mis à jour
    con.remove()
    con = ConnectionPatch(
        xyA=(angle, np.sin(angle)),
        xyB=(np.cos(angle), np.sin(angle)),
        coordsA="data",
        coordsB="data",
        axesA=ax[1],
        axesB=ax[0],
        color="tab:orange",
        lw=1.5,
    )

    ax[1].add_artist(con)


def animate(i, line1, line2):
    if i <= 90:
        set_angle(i * 2 * np.pi / 90, line1, line2)
    else:
        set_angle(2 * np.pi * (2 - i / 90), line1, line2)
    pbar.update()
    return [line1, line2, con]


frames = 180
anim = animation.FuncAnimation(
    fig,
    animate,
    frames=frames,
    interval=100,
    blit=True,
    fargs=[line1, line2],
)

pbar = tqdm(total=frames)
anim.save("fig18.mp4")

pbar = tqdm(total=frames)
anim.save("fig18.gif", writer="imagemagick", fps=100)
