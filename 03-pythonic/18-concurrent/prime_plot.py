# %%
import pandas as pd

times = pd.DataFrame.from_records(
    [
        {
            "py": "3.12.6",
            "type": "séquentiel",
            "duration": pd.Timedelta("0:00:02.631204"),
            "opacity": 0.8,
        },
        {
            "py": "3.12.6",
            "type": "multi-threads",
            "duration": pd.Timedelta("0:00:02.558669"),
            "speedup": 1.028,
            "opacity": 1,
        },
        {
            "py": "3.12.6",
            "type": "multi-interpréteurs",
            "duration": pd.Timedelta("0:00:01.009131"),
            "speedup": 2.607,
            "opacity": 1,
        },
        {
            "py": "3.12.6",
            "type": "multi-processus",
            "duration": pd.Timedelta("0:00:01.129655"),
            "speedup": 2.329,
            "opacity": 0.5,
        },
        {
            "py": "3.13.0rc2",
            "type": "séquentiel",
            "duration": pd.Timedelta("0:00:02.582798"),
            "opacity": 0.8,
        },
        {
            "py": "3.13.0rc2",
            "type": "multi-threads",
            "duration": pd.Timedelta("0:00:02.661552"),
            "speedup": 0.970,
            "opacity": 1,
        },
        {
            "py": "3.13.0rc2",
            "type": "multi-interpréteurs",
            "duration": pd.Timedelta("0:00:01.135046"),
            "speedup": 2.276,
            "opacity": 1,
        },
        {
            "py": "3.13.0rc2",
            "type": "multi-processus",
            "duration": pd.Timedelta("0:00:01.078890"),
            "speedup": 2.394,
            "opacity": 1,
        },
        {
            "py": "3.13.0rc2+nogil",
            "type": "séquentiel",
            "duration": pd.Timedelta("0:00:02.755761"),
            "opacity": 0.8,
        },
        {
            "py": "3.13.0rc2+nogil",
            "type": "multi-threads",
            "duration": pd.Timedelta("0:00:01.128581"),
            "speedup": 2.442,
            "opacity": 1,
        },
        {
            "py": "3.13.0rc2+nogil",
            "type": "multi-interpréteurs",
            "duration": pd.Timedelta("0:00:01.240335"),
            "speedup": 2.222,
            "opacity": 1,
        },
        {
            "py": "3.13.0rc2+nogil",
            "type": "multi-processus",
            "duration": pd.Timedelta("0:00:01.309903"),
            "speedup": 2.104,
            "opacity": 1,
        },
    ]
)

# %%
import altair as alt

alt.Chart(times.eval("duration = duration.dt.total_seconds()")).mark_bar().encode(
    color=alt.Color(
        "type",
        scale=alt.Scale(
            domain=[
                "séquentiel",
                "multi-threads",
                "multi-interpréteurs",
                "multi-processus",
            ]
        ),
        legend=None,
    ),
    row=alt.Row("py", title=None),
    y=alt.Y(
        "type",
        scale=alt.Scale(
            domain=[
                "séquentiel",
                "multi-threads",
                "multi-interpréteurs",
                "multi-processus",
            ]
        ),
        title=None,
    ),
    x=alt.X("duration", title="Temps d'exécution (en s) → "),
    # opacity=alt.Opacity("opacity", scale=alt.Scale(domain=(0, 1)), legend=None),
).properties(width=500).configure_header(
    labelOrient="top",
    labelAnchor="start",
    labelFontWeight="bold",
    labelFontSize=15,
    labelFont="Fira Sans",
).configure_axis(
    labelFontSize=13,
    titleFontSize=14,
    titleAnchor="end",
    titleFont="Fira Sans",
    labelFont="Fira Sans",
)

# %%
import cairosvg

cairosvg.svg2pdf(url="concurrent.svg", write_to="concurrent.pdf")

# %%
