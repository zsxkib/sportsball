"""Aussportsbetting venue model."""

import datetime

import requests

from ...cache import MEMORY
from ..google.google_address_model import create_google_address_model
from ..venue_model import VenueModel


@MEMORY.cache(ignore=["session"])
def create_aussportsbetting_venue_model(
    venue: str, session: requests.Session, dt: datetime.datetime
) -> VenueModel:
    """Create a venue model based off aus sports betting."""
    address_model = create_google_address_model(venue, session, dt)
    return VenueModel(
        identifier=venue,
        name=venue,
        address=address_model,
        is_grass=None,
        is_indoor=None,
    )
