from concurrent.futures import Future, ThreadPoolExecutor, as_completed
from typing import Dict

import requests

import pandas as pd

r = requests.get("https://flagcdn.com/fr/codes.json")
codes = r.json()

start = pd.Timestamp("now")
with ThreadPoolExecutor(max_workers=len(codes)) as executor:
    futures: Dict[Future, str] = dict()

    for code in codes:
        futures[
            executor.submit(requests.get, f"https://flagcdn.com/256x192/{code}.png")
        ] = code

    for future in as_completed(futures):
        data = future.result()

duration = pd.Timestamp("now") - start
print(f"Terminé en {duration}")
