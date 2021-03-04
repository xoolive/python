import matplotlib.pyplot as plt

fig, ax = plt.subplots(
    ncols=2, nrows=2, constrained_layout=True, figsize=(5, 5)
)

# Ajustements supplémentaires

for ax_ in ax.ravel():
    for tick in ax_.xaxis.get_major_ticks() + ax_.yaxis.get_major_ticks():
        tick.label.set_fontsize(14)
        tick.label.set_fontname("Ubuntu")

fig.savefig("fig2.png", bbox_inches="tight")

plt.show()
