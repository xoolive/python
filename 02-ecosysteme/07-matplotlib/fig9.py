import matplotlib.pyplot as plt
import numpy as np

np.random.seed(196801)
exp = np.random.exponential(size=100)

fig, ax = plt.subplots(figsize=(8, 6))

ax.hist(
    exp,
    bins=20,
    edgecolor="white",
    linewidth=2,
    density=True,
    label="ax.hist()",
)
ax.scatter(
    exp,
    np.random.uniform(0, 1, len(exp)) * np.exp(-exp),
    color="black",
    edgecolor="white",
    linewidth=1.5,
    zorder=2,
    label="ax.scatter()",
)

x = np.linspace(0, 6, 100)
y = np.exp(-x)
ax.plot(x, y, color="white", linewidth=6)
ax.plot(x, y, color="crimson", linewidth=3, label="ax.plot()")

ax.legend(
    prop={"family": "Ubuntu", "size": 16},
    borderpad=0.5,
)

for tick in ax.xaxis.get_major_ticks() + ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(16)
    tick.label.set_fontname("Ubuntu")

fig.savefig("fig9_1.png", bbox_inches="tight")
plt.show()

fig, ax = plt.subplots(figsize=(6, 6))

x, y = np.meshgrid(np.linspace(0, 5, 100), np.linspace(0, 5, 100))
z = np.sin(x) ** 10 + np.cos(10 + y * x) * np.cos(x)

img = ax.imshow(z, extent=[0, 5, 0, 5], origin="lower", alpha=0.5)
contours = ax.contour(x, y, z, 3, colors="black")
ax.clabel(contours, inline=True, fontsize=12)

cax = plt.axes([1, 0.2, 0.04, 0.6])
cbar = fig.colorbar(img, cax=cax)

for tick in cbar.ax.get_ymajorticklabels():
    tick.set_fontsize(16)
    tick.set_fontname("Ubuntu")

for tick in ax.xaxis.get_major_ticks() + ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(16)
    tick.label.set_fontname("Ubuntu")

fig.savefig("fig9_2.png", bbox_inches="tight")
plt.show()