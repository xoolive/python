import logging

import click
import requests

from .core.api import api_points
from .core.utils import readtime


@click.command(help="Les titres diffusés sur FIP")
@click.argument("radio", type=str, default="FIP")
@click.option(
    "-a",
    "--all",
    "all_",
    default=False,
    is_flag=True,
    help="Afficher tous les morceaux",
)
@click.option("--next", "next_", is_flag=True, default=False)
@click.option("--previous", is_flag=True, default=False)
@click.option("-v", "--verbose", count=True, help="Niveau de verbosité (debug)")
def main(
    radio: str,
    next_: bool,
    previous: bool,
    all_: bool,
    current: bool = True,
    verbose: int = 0,
):

    logger = logging.getLogger()
    if verbose == 1:
        logger.setLevel(logging.INFO)
    elif verbose > 1:
        logger.setLevel(logging.DEBUG)

    response = requests.get(api_points[radio])
    response.raise_for_status()

    for i, elt in enumerate(reversed(response.json()["steps"].values())):
        if (
            all_
            or (i == 0 and next_)
            or (i == 1 and current)
            or (i == 2 and previous)
        ):
            if i == 1 and current:
                print("[*] ", end="")
            else:
                print("    ", end="")
            print(f"{readtime(elt['start'])} -> {readtime(elt['end'])}", end="")
            print(f" {elt['title']} par {elt['authors']}", end="")
            print(f" ({elt['titreAlbum']})")


if __name__ == "__main__":
    main()
