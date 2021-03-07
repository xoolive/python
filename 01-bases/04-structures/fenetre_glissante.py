from collections import deque


def fenetre_glissante(sequence, k):
    """Calcule une moyenne sur des fenêtres glissantes.
    k est la taille de la fenêtre glissante

    >>> fenetre_glissante([40, 30, 50, 46, 39, 44], 3)
    [40.0, 42.0, 45.0, 43.0]
    """
    d = deque(sequence[:k])  # on initialise avec les k premiers élements
    avg, s = [], sum(d)
    avg.append(s / k)  # la moyenne sur la fenêtre

    for elt in sequence[k:]:
        s += elt - d.popleft()  # on enlève la 1re valeur, on ajoute la nouvelle
        d.append(elt)
        avg.append(s / k)

    return avg


print(fenetre_glissante([40, 30, 50, 46, 39, 44], 3))
