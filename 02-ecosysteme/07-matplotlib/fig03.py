import matplotlib.pyplot as plt

fig = plt.figure(figsize=(5, 3))
ax1 = fig.add_axes([0, 0, 1, 1])
ax2 = fig.add_axes([0.65, 0.65, 0.2, 0.2])

# Ajustements supplémentaires
title_style = dict(pad=10, fontname="Ubuntu", fontsize=18)

ax1.set_title("ax1", **title_style)
ax2.set_title("ax2", **title_style)


# Ajustements supplémentaires

for ax_ in [ax1, ax2]:
    for tick in ax_.xaxis.get_major_ticks() + ax_.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)
        tick.label.set_fontname("Ubuntu")

fig.savefig("fig03.png", bbox_inches="tight")
plt.show()
