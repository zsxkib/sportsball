"""NCAAB sports reference player model."""

from urllib.parse import unquote

import requests
from bs4 import BeautifulSoup

from ....cache import MEMORY
from ....session import DEFAULT_TIMEOUT
from ...player_model import PlayerModel


def _fix_url(url: str) -> str:
    url = unquote(url)
    url = url.replace("Ã©", "é")
    return url


@MEMORY.cache(ignore=["session"])
def create_ncaab_sportsreference_player_model(
    session: requests.Session,
    player_url: str,
) -> PlayerModel:
    """Create a player model from NCAAB sports reference."""
    player_url = _fix_url(player_url)
    response = session.get(player_url, timeout=DEFAULT_TIMEOUT)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    h1 = soup.find("h1")
    if h1 is None:
        raise ValueError("h1 is null.")
    name = h1.get_text().strip()
    return PlayerModel(identifier=name, jersey=None, kicks=None, fumbles=None)
