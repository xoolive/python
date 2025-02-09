import time
from typing import Optional

import pandas as pd


def readtime(ts: int, tz: Optional[str] = None) -> str:
    """Convert unix timestamp to human readable time.

    >>> readtime(1609459200, tz="UTC")
    '00:00'
    """
    if tz is None:
        tz = time.tzname[0]
    return f"{pd.Timestamp(ts, unit='s', tz='utc').tz_convert(tz):%H:%M}"


def wrap(text: str, size: int) -> str:
    if len(text) <= size:
        return text
    return text[: size - 3] + "..."
