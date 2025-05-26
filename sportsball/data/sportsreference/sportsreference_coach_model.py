"""Sports reference coach model."""

# pylint: disable=duplicate-code
import os
from urllib.parse import urlparse
import logging

import pytest_is_running
import requests_cache
from bs4 import BeautifulSoup

from ...cache import MEMORY
from ..coach_model import CoachModel
from ...proxy_session import X_NO_WAYBACK

_NON_WAYBACK_URLS: set[str] = {
    "https://www.sports-reference.com/cbb/coaches/kelvin-sampson-1.html",
    "https://www.sports-reference.com/cbb/coaches/fred-hoiberg-1.html",
    "https://www.sports-reference.com/cbb/coaches/johnny-dawkins-1.html",
    "https://www.sports-reference.com/cbb/coaches/bruce-pearl-1.html",
    "https://www.sports-reference.com/cbb/coaches/leon-rice-1.html",
    "https://www.sports-reference.com/cbb/coaches/wes-miller-1.html",
}


def _create_sportsreference_coach_model(
    session: requests_cache.CachedSession, coach_url: str
) -> CoachModel:
    """Create a coach model from sports reference."""
    headers = {}
    if coach_url in _NON_WAYBACK_URLS:
        headers = {X_NO_WAYBACK: "1"}
    response = session.get(coach_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")
    name = None
    for h1 in soup.find_all("h1"):
        for span in h1.find_all("span"):
            name = span.get_text().strip()
            break
        if name is not None:
            break
    if name is None:
        logging.error("error url = %s", coach_url)
        raise ValueError("name is null")
    o = urlparse(coach_url)
    last_component = o.path.split("/")[-1]
    identifier, _ = os.path.splitext(last_component)
    return CoachModel(
        identifier=identifier,
        name=name,
    )


@MEMORY.cache(ignore=["session"])
def _cached_create_sportsreference_coach_mode(
    session: requests_cache.CachedSession,
    coach_url: str,
) -> CoachModel:
    return _create_sportsreference_coach_model(session, coach_url)


def create_sportsreference_coach_model(
    session: requests_cache.CachedSession,
    coach_url: str,
) -> CoachModel:
    """Create a coach model from sports reference."""
    if not pytest_is_running.is_running():
        return _cached_create_sportsreference_coach_mode(session, coach_url)
    with session.cache_disabled():
        return _create_sportsreference_coach_model(session, coach_url)
