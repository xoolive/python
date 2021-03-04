import matplotlib.pyplot as plt

fig = plt.figure(constrained_layout=True)
ax = fig.add_subplot()

ax.grid()  # ajoute les guides

ax.set_xticks(range(10))
ax.set_ylim((0.1, 100))
ax.set_yscale("log")  # axe logarithmique


# Ajustements supplémentaires

ax.set_title("ax.set_title(txt)", pad=15, fontname="Ubuntu", fontsize=18)
ax.set_xlabel("ax.set_xlabel(txt)", labelpad=5, fontname="Ubuntu", fontsize=16)
ax.set_ylabel("ax.set_ylabel(txt)", fontname="Ubuntu", fontsize=16)

for tick in ax.xaxis.get_major_ticks() + ax.yaxis.get_major_ticks():
    tick.label.set_fontsize(14)
    tick.label.set_fontname("Ubuntu")

fig.suptitle("fig.suptitle(txt)", fontname="Ubuntu", fontsize=18)
fig.savefig("fig1.png", bbox_inches="tight")

plt.show()
