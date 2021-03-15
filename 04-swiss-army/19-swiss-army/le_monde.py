import re
import requests
from bs4 import BeautifulSoup

c = requests.get("https://www.lemonde.fr/")
c.raise_for_status()
contenu = BeautifulSoup(c.text, "lxml")

print("Le Monde")
print("========")

for x in contenu.find_all(attrs={"class": "area--section"}):
    header = x.find("h4")
    if header is not None:
        print(header.text.strip())

print()

print("International")
print("-------------")
# L'expression régulière permet de s'affranchir des espaces
intl = contenu.find("h4", text=re.compile("International"))
# On recherche un nœud parmi les parents (celui qui englobe le titre)
section = intl.find_parent(attrs={"class": "area--section"})
title_attrs = {"class": "article__title"}
# Trouver les titres de chaque article de la section
# On tronque les titres après 65 caractères
for i, art in enumerate(section.find_all(attrs=title_attrs), 1):
    print(f"{i}. {art.text}")