import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import g
from scipy.integrate import solve_ivp


def forces(t, state, g):
    g_vec = np.array([0, -g])  # metres per second
    dstate = state.copy()
    dstate[:2] = state[2:]  # vitesse
    dstate[2:] = g_vec  # accélération
    return dstate


state0 = np.array([0.0, 100.0, 100.0, 100.0])
t = np.arange(0.0, 25.0, 0.1)

sol = solve_ivp(forces, (t.min(), t.max()), state0, t_eval=t, args=(g,))

fig, ax = plt.subplots(
    figsize=(7, 4),
)
ax.plot(sol.y[0, :], sol.y[1, :], lw=2, label="solve_ivp(...)")

scale = 3
ax.arrow(
    *state0[:2],
    *scale * state0[2:],
    lw=2,
    head_width=scale * 10,
    head_length=scale * 15,
    zorder=2
)


def touche_le_sol(t, y, g):
    return y[1]


touche_le_sol.terminal = True

sol = solve_ivp(
    forces,
    (t.min(), t.max()),
    state0,
    t_eval=t,
    args=(g,),
    events=touche_le_sol,
)

ax.plot(
    sol.y[0, :], sol.y[1, :], lw=2, label="solve_ivp(..., events=touche_le_sol)"
)
# ax[1].set_title("events=hit_ground", fontname="Ubuntu", fontsize=16, pad=7)

ax.plot(sol.y_events[0][0, 0], sol.y_events[0][0, 1], "C1o", ms=10)

ax.legend(
    loc=(0.1, 0),
    prop={
        "family": "Ubuntu",
        "size": 15,
    },
    borderpad=0.5,
)
for ax_ in [ax]:
    ax_.spines["left"].set_position("zero")
    ax_.spines["bottom"].set_position("zero")
    ax_.spines["right"].set_visible(False)
    ax_.spines["top"].set_visible(False)

    ax_.tick_params(pad=7)

    for tick in ax_.xaxis.get_major_ticks() + ax_.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)
        tick.label.set_fontname("Ubuntu")

fig.savefig("fig03.png", bbox_inches="tight")

plt.show()
