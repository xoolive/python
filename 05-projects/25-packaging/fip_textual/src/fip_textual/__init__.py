import logging
import time
import webbrowser
from typing import NotRequired, TypedDict

import httpx
import pandas as pd
from rich.text import Text
from textual import events
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.logging import TextualHandler
from textual.widgets import Button, Footer, Header, Label

logging.basicConfig(handlers=[TextualHandler()])


class EntryContent(TypedDict):
    title: str
    start: int
    end: int
    authors: str
    anneeEditionMusique: NotRequired[int]
    lienYoutube: NotRequired[str]
    titleAlbum: str
    label: str
    composers: str
    visual: str  # url to the image


class FipResult(TypedDict):
    steps: dict[str, EntryContent]
    station_id: int


def readtime(ts: int) -> str:
    """Convert unix timestamp to human readable time"""
    tz = time.tzname[0]
    return f"{pd.Timestamp(ts, unit='s', tz='utc').tz_convert(tz):%H:%M}"


class TextDisplay(Label):
    def __init__(self, text, id=None, **kwargs):
        self.text = text
        self.kwargs = kwargs
        self.width = len(text) + 2
        super().__init__(id=id)

    def compose(self) -> ComposeResult:
        label = Label(Text(self.text, **self.kwargs))
        label.width = self.width
        yield label


class Entry(Button):
    BINDINGS = [("enter", "enter", "Ouvrir dans YouTube")]

    def __init__(self, elt: EntryContent, id=None):
        self.elt = elt
        super().__init__(id=id)

    async def action_enter(self) -> None:
        if "lienYoutube" in self.elt.keys():
            webbrowser.open(self.elt["lienYoutube"])

    def compose(self) -> ComposeResult:
        yield Horizontal(
            Vertical(
                TextDisplay(readtime(self.elt["start"]), id="start"),
                TextDisplay(readtime(self.elt["end"]), id="end"),
                id="heures",
            ),
            Vertical(
                Horizontal(
                    TextDisplay(self.elt["title"], id="titre"),
                    TextDisplay(" | ", id="separator"),
                    TextDisplay(self.elt.get("titreAlbum", ""), id="album"),
                    TextDisplay(
                        str(self.elt.get("anneeEditionMusique", "")), id="annee"
                    ),
                    id="titre_album",
                ),
                Horizontal(
                    TextDisplay(self.elt.get("authors", ""), id="authors"),
                    TextDisplay(self.elt.get("label", ""), id="label"),
                    id="auteurs",
                ),
            ),
        )


class FipTextual(App):
    BINDINGS = [
        ("q,escape", "quit", "Quitter"),
        ("r", "retrieve", "Rafraîchir"),
    ]
    CSS_PATH = "fip.tcss"

    def on_load(self, _event: events.Load) -> None:
        self.title = "FIP"
        self.async_client = httpx.AsyncClient()

    async def on_mount(self) -> None:
        await self.action_retrieve()
        self.timer = self.set_interval(60, self.action_retrieve)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
        yield VerticalScroll(id="entries")

    async def action_retrieve(self):
        url = "https://api.radiofrance.fr/livemeta/pull/66"
        r = await self.async_client.get(url)
        try:
            r.raise_for_status()
            self.json = r.json()
        except httpx.HTTPStatusError as e:
            self.notify(f"HTTP error: {e}", severity="error")

        vertical_scroll = self.query_one(VerticalScroll)

        for elt in self.json["steps"].values():
            if elt["title"] not in [e.elt["title"] for e in vertical_scroll.children]:
                child = Entry(elt)
                vertical_scroll.mount(child)
                if "lienYoutube" in elt.keys():
                    child.add_class("youtube")
                child.focus()


def main() -> None:
    app = FipTextual()
    app.run()


if __name__ == "__main__":
    main()
