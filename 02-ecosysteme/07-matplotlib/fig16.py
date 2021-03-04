import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure(figsize=(12, 8))
linear = np.linspace(0, 10, 100)
fig.subplots_adjust(wspace=0.2, hspace=0.3)

for elt, style in zip(
    [221, 222, 223, 224],
    ["default", "seaborn", "ggplot", "fivethirtyeight"],
):
    with plt.style.context(style):

        ax = fig.add_subplot(elt)

        ax.plot(linear, np.sin(linear))
        ax.plot(linear, np.cos(linear))

        ax.set_title(
            f'with plt.style.context("{style}")',
            pad=10,
            fontsize=16,
            fontname="Ubuntu",
        )

        for tick in ax.xaxis.get_major_ticks() + ax.yaxis.get_major_ticks():
            tick.label.set_fontsize(14)
            tick.label.set_fontname("Ubuntu")

fig.savefig("fig16.png", bbox_inches="tight")
plt.show()