from threading import Thread

import requests

import pandas as pd

r = requests.get("https://flagcdn.com/fr/codes.json")
codes = r.json()


class Drapeau(Thread):
    def __init__(self, code):
        super().__init__()
        self.code = code

    def run(self):
        url = f"https://flagcdn.com/256x192/{self.code}.png"
        self.r = requests.get(url)


threads = []

start = pd.Timestamp("now")
for c in codes.keys():
    thread = Drapeau(c)
    thread.start()
    threads.append(thread)

for thread in threads:
    thread.join()

duration = pd.Timestamp("now") - start
print(f"Terminé en {duration}")
