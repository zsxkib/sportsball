"""AFL AFLTables venue model."""

import datetime
import os
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from ....cache import MEMORY
from ...google.google_address_model import create_google_address_model
from ...venue_model import VenueModel


@MEMORY.cache(ignore=["session"])
def create_afl_afltables_venue_model(
    url: str, session: requests.Session, dt: datetime.datetime
) -> VenueModel:
    """Create a venue model from AFL tables."""
    o = urlparse(url)
    last_component = o.path.split("/")[-1]
    identifier, _ = os.path.splitext(last_component)
    response = session.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    name = None
    for h1 in soup.find_all("h1"):
        name = h1.get_text()
    if name is None:
        raise ValueError("name is null.")
    address = create_google_address_model(f"{name} - Australia", session, dt)
    return VenueModel(
        identifier=identifier,
        name=name,
        address=address,  # pyright: ignore
        is_grass=None,
        is_indoor=None,
    )
