"""NFL SportsDB venue model."""

import datetime

import requests

from ....cache import MEMORY
from ...google.google_address_model import create_google_address_model
from ...venue_model import VenueModel


@MEMORY.cache(ignore=["session"])
def create_nfl_sportsdb_venue_model(
    session: requests.Session, venue_id: str, dt: datetime.datetime
) -> VenueModel | None:
    """Create NFL sports DB venue model."""
    if venue_id == "19533":
        venue_id = "17146"
    if venue_id == "21813":
        venue_id = "23848"
    if venue_id == "21642":
        venue_id = "29570"
    if venue_id == "23652":
        venue_id = "29569"
    if venue_id == "23654":
        venue_id = "15874"
    if venue_id == "23655":
        venue_id = "30856"
    if venue_id == "23656":
        venue_id = "29575"
    if venue_id == "23657":
        venue_id = "23720"
    response = session.get(
        f"https://www.thesportsdb.com/api/v1/json/3/lookupvenue.php?id={venue_id}"
    )
    response.raise_for_status()
    venues = response.json()["venues"]
    if venues is None:
        return None
    venue = venues[0]
    name = venue["strVenue"]

    address = create_google_address_model(
        " - ".join(
            [
                x
                for x in [
                    name,
                    venue["strLocation"],
                    venue["strCountry"],
                ]
                if x is not None and x
            ]
        ),
        session,
        dt,
    )

    return VenueModel(
        identifier=venue_id,
        name=name,
        address=address,  # pyright: ignore
        is_grass=None,
        is_indoor=None,
    )
