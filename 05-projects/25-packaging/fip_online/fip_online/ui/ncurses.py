import curses
import webbrowser

import requests

from ..core.utils import readtime, wrap


class FIPScreen:
    header = (
        " FIP ('q' or Ctrl+C pour quitter, Entrée pour accéder à la vidéo) "
    )

    def __init__(self):
        self.init_curses()
        self.retrieve()

        self.idx = 0
        self.cursor_x = 3

    @property
    def cursor_y(self):
        return 2 * self.idx + 3

    def init_curses(self):
        self.screen = curses.initscr()
        self.screen.keypad(True)

        curses.noecho()
        curses.mousemask(True)

    def draw_frame(self):
        self.screen.border(0)
        self.screen.addstr(0, 2, self.header)

        for i, elt in enumerate(self.json["steps"].values()):
            self.screen.addstr(2 * i + 3, 2, "[ ]")
            self.screen.addstr(2 * i + 3, 6, readtime(elt["start"]))
            self.screen.addstr(2 * i + 3, 12, readtime(elt["end"]))
            self.screen.addstr(2 * i + 3, 18, wrap(elt["title"], 20))
            self.screen.addstr(2 * i + 3, 39, wrap(elt["authors"], 15))
            self.screen.addstr(2 * i + 3, 55, wrap(elt["titreAlbum"], 15))
            self.screen.addstr(
                2 * i + 3, 71, str(elt.get("anneeEditionMusique", ""))
            )

        self.reset_cursor_position()

    def reset_cursor_position(self):
        self.screen.move(self.cursor_y, self.cursor_x)

    def retrieve(self):
        url = "https://api.radiofrance.fr/livemeta/pull/7"
        response = requests.get(url)
        try:
            response.raise_for_status()
        except Exception:
            pass
        else:
            self.json = response.json()
            self.n = len(self.json["steps"])

    def run(self):
        while True:
            self.screen.clear()
            self.draw_frame()
            self.screen.refresh()
            c = self.screen.getch()

            if c in [curses.KEY_F5, ord("r"), ord("R")]:
                self.retrieve()
            elif c in [curses.KEY_DOWN, ord("j")]:
                self.idx = self.idx + 1 if self.idx < self.n - 1 else self.idx
            elif c in [curses.KEY_UP, ord("k")]:
                self.idx = self.idx - 1 if self.idx > 0 else 0
            elif c in [10, ord("y")]:  # ENTER, y
                elt = list(self.json["steps"].values())[self.idx]
                youtube_link = elt.get("lienYoutube", None)
                if youtube_link:
                    webbrowser.open(youtube_link)
            elif c in [27, ord("q"), ord("Q")]:  # ESC, q
                raise KeyboardInterrupt


def main():
    try:
        screen = FIPScreen()
        screen.run()
    except KeyboardInterrupt:
        pass
    finally:
        curses.endwin()
