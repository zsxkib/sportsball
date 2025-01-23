"""Venue model from wikipedia information."""

import logging

import requests
import wikipediaapi  # type: ignore

from ... import __VERSION__
from ...cache import MEMORY
from ..venue_model import VenueModel

WIKIPEDIA_VENUE_ID_MAP: dict[str, str] = {}


@MEMORY.cache(ignore=["session"])
def create_wikipedia_venue_model(
    session: requests.Session, identifier: str
) -> VenueModel | None:
    """Create a venue model by looking up the venue on wikipedia."""
    # pylint: disable=protected-access

    wikipage = WIKIPEDIA_VENUE_ID_MAP.get(identifier)
    if wikipage is None:
        logging.warning(
            "Failed to map wikipedia venue for venue identifier: %s", identifier
        )
        return None

    wiki_wiki = wikipediaapi.Wikipedia(user_agent=f"sportsball ({__VERSION__})")
    wiki_wiki._session = session
    page_py = wiki_wiki.page(wikipage)

    return VenueModel(
        identifier=wikipage,
        name=page_py.title,
        address=None,
        is_grass=None,
        is_indoor=None,
    )
