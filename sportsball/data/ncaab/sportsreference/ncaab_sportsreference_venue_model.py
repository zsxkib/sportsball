"""NCAAB Sports Reference venue model."""

import datetime

import requests

from ....cache import MEMORY
from ...google.google_address_model import create_google_address_model
from ...venue_model import VenueModel


@MEMORY.cache(ignore=["session"])
def create_ncaab_sportsreference_venue_model(
    venue_name: str, session: requests.Session, dt: datetime.datetime
) -> VenueModel | None:
    """Create an NCAAB sports reference venue model."""
    if not venue_name:
        return None
    address_model = create_google_address_model(venue_name, session, dt)
    return VenueModel(
        identifier=venue_name,
        name=venue_name,
        address=address_model,
        is_grass=None,
        is_indoor=None,
    )
