import matplotlib.pyplot as plt


def syracuse(n: int) -> "generator":
    """Calcule la suite de Syracuse.

    >>> list(p for p in syracuse(28))
    [28, 14, 7, 22, 11, 34, 17, 52, 26, 13, 40, 20, 10, 5, 16, 8, 4, 2, 1]
    """
    yield n
    while n != 1:
        if n & 1 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        yield n


print(list(syracuse(27)))

fig, ax = plt.subplots()
ax.plot(list(syracuse(27)), "k")
ax.tick_params(
    which="major",  # sélection
    direction="in",
    length=7,
    width=1.5,  # style
    labelsize=14,
    pad=10,
)
ax.set_title(
    "Parcours de la suite de Syracuse initialisée à 27",
    fontname="Ubuntu",
    fontsize=16,
)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_linewidth(1.5)
ax.spines["left"].set_linewidth(1.5)

fig.savefig("syracuse_27.png")
plt.show()


def length(iterable):
    "Renvoie la longueur d'une structure itérable finie."
    return sum(1 for _ in iterable)


fig, ax = plt.subplots()
interval = range(1, 1000)
ax.plot(interval, [length(syracuse(i)) for i in interval], "k.")
ax.tick_params(
    which="major",  # sélection
    direction="in",
    length=7,
    width=1.5,  # style
    labelsize=14,
    pad=10,
)
ax.set_title("Longueur de la suite de Syracuse", fontname="Ubuntu", fontsize=16)
ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_linewidth(1.5)
ax.spines["left"].set_linewidth(1.5)
fig.savefig("syracuse_length.png")
plt.show()

fig, ax = plt.subplots()
ax.set_yscale("log")
ax.set_yticks([1 << i for i in range(1, 17)])
ax.set_yticklabels([1 << i for i in range(1, 17)])

interval = range(1, 200)
ax.plot(interval, [max(syracuse(i)) for i in interval], "k.")

ax.set_title(
    "Hauteur de la suite de la Syracuse", fontname="Ubuntu", fontsize=16
)

ax.tick_params(
    which="major",  # sélection
    direction="in",
    length=7,
    width=1.5,  # style
    labelsize=14,
    pad=10,
)

ax.spines["right"].set_visible(False)
ax.spines["top"].set_visible(False)
ax.spines["bottom"].set_linewidth(1.5)
ax.spines["left"].set_linewidth(1.5)
fig.savefig("syracuse_height.png")
plt.show()
