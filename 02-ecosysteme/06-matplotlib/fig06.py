import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(2, 2, figsize=(10, 7))

np.random.seed(196801)

title_style = dict(pad=10, fontname="Ubuntu", fontsize=16)

linear = np.linspace(0, 10, 100)
ax[0, 0].plot(linear, np.sin(linear))
ax[0, 0].set_title("ax.plot(x, np.sin(x))", **title_style)

exp = np.random.exponential(size=100)
ax[0, 1].hist(exp, bins=20, edgecolor="white", linewidth=2)
ax[0, 1].set_title("ax.hist(x)", **title_style)

x, y = np.random.uniform(size=(2, 50))
ax[1, 0].scatter(x, y, s=60, alpha=0.7, edgecolor="white", linewidth=1)
ax[1, 0].set_title("ax.scatter(x, y)", **title_style)

labels = ["$x_1$", "$x_2$", "$x_3$", "$x_4$"]
colors = ["pink", "lightblue", "lightgreen", "orange"]
data_1 = np.random.normal(100, 10, 200)
data_2 = np.random.normal(90, 20, 200)
data_3 = np.random.normal(80, 30, 200)
data_4 = np.random.normal(70, 40, 200)
data = [data_1, data_2, data_3, data_4]

bp = ax[1, 1].boxplot(data, patch_artist=True, labels=labels, widths=0.25)
for elt, color in zip(bp["boxes"], colors):
    elt.set_facecolor(color)
for elt in bp["medians"]:
    elt.set_color("black")
ax[1, 1].set_title("ax.boxplot(data)", **title_style)

for ax_ in ax.ravel():
    for tick in ax_.xaxis.get_major_ticks() + ax_.yaxis.get_major_ticks():
        tick.label.set_fontsize(14)
        tick.label.set_fontname("Ubuntu")

fig.subplots_adjust(hspace=0.3)
fig.savefig("fig06.png", bbox_inches="tight")

plt.show()
