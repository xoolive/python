from pyodide.http import open_url
from pyscript import display

import pandas as pd
import altair as alt

url = "https://raw.githubusercontent.com/datasets/airport-codes/master/data/airport-codes.csv"

df = (
    pd.read_csv(open_url(url))
    .eval("""
latitude = coordinates.str.split(",").str[0].astype("float")
longitude = coordinates.str.split(",").str[1].astype("float")
""")
    .query("ident.str.startswith('LF') and longitude > -5 and longitude < 15")
)

display(df, target="airport-codes")
print(df.query("ident.str.startswith('LF')").head())

chart = (
    alt.Chart(df)
    .mark_point()
    .encode(latitude="latitude", longitude="longitude")
    .project("conicConformal", rotate=[-3, -46.5], parallels=[49, 44])
)

display(chart, target="altair-output")
