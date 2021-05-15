import pandas as pd
import requests

from flask import Flask, request
from flask.templating import render_template

from ..core.api import api_points
from ..core.utils import readtime

app = Flask(__name__)
app.debug = True
app.jinja_env.globals.update(readtime=readtime)


@app.route("/time", methods=["GET"])
def now():
    now = pd.Timestamp("now", unit="s", tz="utc")
    tz = request.args.get("tz", None)
    if tz is not None:
        now = now.tz_convert(tz)
    return {"time": f"{now}"}


@app.route("/", methods=["GET", "POST"])
def index():
    radio = request.form["radio"] if request.method == "POST" else "FIP"
    response = requests.get(api_points[radio])
    response.raise_for_status()
    results = list(response.json()["steps"].values())

    return render_template(
        "index.html", radio=radio, results=results, api_points=api_points.keys()
    )


def main():
    app.run(host="0.0.0.0", port=7812)
