import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import G
from scipy.integrate import solve_ivp


def forces(t, state, m1, m2):  # replace y by z
    x1, y1, vx1, vy1, x2, y2, vx2, vy2 = state
    ss1 = np.array([x2 - x1, y2 - y1])
    r3 = (ss1 * ss1).sum()
    r3 *= np.sqrt(r3)
    return np.r_[vx1, vy1, G * m2 / r3 * ss1, vx2, vy2, -G * m1 / r3 * ss1]


s1, m1 = np.array([10.0, 0.0, 0.0, -1.0]), 8e11
s2, m2 = np.array([-8, 0, 0, 0.8]), 1e12

state0 = np.r_[s1, s2]
t = np.arange(0.0, 100.0, 0.1)

fig, ax = plt.subplots(1, 2, figsize=(10, 4))

fig.subplots_adjust(
    wspace=0.1,
)
sol = solve_ivp(
    forces, (t.min(), t.max()), state0, t_eval=t, method="RK45", args=(m1, m2)
)


ax[0].plot(sol.y[0, :], sol.y[1, :], sol.y[4, :], sol.y[5, :])
ax[0].set_title('method="RK45"', fontname="Ubuntu", fontsize=18)

ax_in = ax[0].inset_axes([0.505, 0.51, 0.35, 0.35])
ax_in.set_xlim((8.5, 10.5))
ax_in.set_ylim((-1, 1))
ax_in.xaxis.set_major_locator(plt.NullLocator())
ax_in.yaxis.set_major_locator(plt.NullLocator())
for s in ax_in.spines.values():
    s.set_linewidth(2)

ax[0].indicate_inset_zoom(ax_in, lw=2)
ax_in.plot(sol.y[0, :], sol.y[1, :], sol.y[4, :], sol.y[5, :])


sol = solve_ivp(
    forces, (t.min(), t.max()), state0, t_eval=t, method="DOP853", args=(m1, m2)
)

ax[1].plot(
    sol.y[0, :],
    sol.y[1, :],
    sol.y[4, :],
    sol.y[5, :],
)
ax[1].set_title('method="DOP853"', fontname="Ubuntu", fontsize=18)

ax_in = ax[1].inset_axes([0.505, 0.51, 0.35, 0.35])
ax_in.set_xlim((8.5, 10.5))
ax_in.set_ylim((-1, 1))
ax_in.xaxis.set_major_locator(plt.NullLocator())
ax_in.yaxis.set_major_locator(plt.NullLocator())
for s in ax_in.spines.values():
    s.set_linewidth(2)

ax[1].indicate_inset_zoom(ax_in, lw=2)
ax_in.plot(sol.y[0, :], sol.y[1, :], sol.y[4, :], sol.y[5, :])
# plt.set_aspect(1)

for ax_ in ax.ravel():

    ax_.spines["left"].set_position("zero")
    ax_.spines["bottom"].set_position("zero")
    ax_.spines["right"].set_visible(False)
    ax_.spines["top"].set_visible(False)

    ax_.tick_params(pad=7)
    for tick in ax_.xaxis.get_major_ticks() + ax_.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)
        tick.label.set_fontname("Ubuntu")

    ax_.xaxis.set_major_locator(plt.MultipleLocator(2))
    ax_.yaxis.set_major_locator(plt.FixedLocator([-4, 4]))

    ax_.set_aspect(1)

fig.savefig("fig04.png", bbox_inches="tight")

plt.show()
