import math
from concurrent.futures import Future, ProcessPoolExecutor, as_completed
from typing import Dict

import pandas as pd

grands_nombres_premiers = [
    112272535095293,
    112582705942171,
    112272535095293,
    115280095190773,
    115797848077099,
    1099726899285419,
]


def nombre_premier(n: int) -> bool:
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True


start = pd.Timestamp("now")
with ProcessPoolExecutor(max_workers=4) as executor:
    futures: Dict[Future, int] = dict()
    results: Dict[int, bool] = dict()
    for prime in grands_nombres_premiers:
        futures[executor.submit(nombre_premier, prime)] = prime
    for future in as_completed(futures):
        results[futures[future]] = future.result()

duration = pd.Timestamp("now") - start
print(f"Terminé en {duration}")
