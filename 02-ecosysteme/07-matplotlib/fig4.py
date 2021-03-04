import matplotlib.pyplot as plt

fig = plt.figure(constrained_layout=True)
gs = fig.add_gridspec(3, 3)

# Ajustements supplémentaires
title_style = dict(pad=10, fontname="Ubuntu", fontsize=16)

ax1 = fig.add_subplot(gs[0, :])
ax1.set_title("gs[0, :]", **title_style)
ax2 = fig.add_subplot(gs[1, :-1])
ax2.set_title("gs[1, :-1]", **title_style)
ax3 = fig.add_subplot(gs[1:, -1])
ax3.set_title("gs[1:, -1]", **title_style)
ax4 = fig.add_subplot(gs[-1, 0])
ax4.set_title("gs[-1, 0]", **title_style)
ax5 = fig.add_subplot(gs[-1, -2])
ax5.set_title("gs[-1, -2]", **title_style)


# Ajustements supplémentaires

for ax_ in [ax1, ax2, ax3, ax4, ax5]:
    for tick in ax_.xaxis.get_major_ticks() + ax_.yaxis.get_major_ticks():
        tick.label.set_fontsize(12)
        tick.label.set_fontname("Ubuntu")

fig.savefig("fig4.png", bbox_inches="tight")

plt.show()
