from datetime import datetime
from zoneinfo import ZoneInfo

timezones = [
    "Africa/Sao_Tome",
    "America/Los_Angeles",
    "America/New_York",
    "Asia/Hong_Kong",
    "Europe/Paris",
    "Pacific/Noumea",
    "Pacific/Tahiti",
]


def saint_sylvestre(tz):
    return datetime(2020, 1, 1, tzinfo=ZoneInfo(tz))


# Qui fête la nouvelle année en premier?
print(sorted(timezones, key=saint_sylvestre))