from ..core.utils import readtime, wrap


def test_readtime() -> None:
    ts = readtime(1609459200, tz="UTC")
    assert ts == "00:00"
    ts = readtime(1609459200, tz="CET")
    assert ts == "01:00"


def test_wrap() -> None:
    assert wrap("tester", 7) == "tester"
    assert wrap("tester", 6) == "tester"
    assert wrap("tester", 5) == "te..."
