from flask import Flask, request
import pandas as pd

app = Flask(__name__)


@app.route("/time", methods=["GET"])
def now():
    now = pd.Timestamp("now", unit="s", tz="utc")
    tz = request.args.get("tz", None)
    if tz is not None:
        now = now.tz_convert(tz)
    return {"time": f"{now}"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=7812)
