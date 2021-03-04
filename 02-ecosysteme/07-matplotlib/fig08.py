import matplotlib.pyplot as plt
import numpy as np

theta = np.linspace(0, 12 * np.pi, 10000)
r = (
    np.exp(np.sin(theta))
    - 2 * np.cos(4 * theta)
    + np.sin((2 * theta - np.pi) / 24) ** 5
)

fig, ax = plt.subplots(figsize=(5, 5), subplot_kw=dict(polar=True))
ax.plot(theta + (r < 0) * np.pi, np.abs(r), alpha=0.7)

ax.set_thetagrids(
    angles=range(0, 360, 30),
    fontsize=14,
    fontname="Ubuntu",
)
ax.set_rgrids(
    radii=range(0, 6, 1),
    angle=15,
    fontsize=14,
    fontname="Ubuntu",
)

fig.savefig("fig08.png", bbox_inches="tight")
plt.show()
