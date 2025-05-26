"""AFL AFLTables coach model."""

# pylint: disable=too-many-locals
import io
import os
import urllib.parse
from urllib.parse import urlparse

import pandas as pd
import pytest_is_running
import requests_cache
from bs4 import BeautifulSoup

from ....cache import MEMORY
from ...coach_model import CoachModel

_COACH_URL_CACHE: dict[str, str] = {}


def _create_afl_afltables_coach_model(
    url: str, session: requests_cache.CachedSession, year: int
) -> CoachModel:
    html = _COACH_URL_CACHE.get(url)
    if html is None:
        with session.cache_disabled():
            response = session.get(url)
            html = response.text
            _COACH_URL_CACHE[url] = html
    handle = io.StringIO()
    handle.write(html)
    handle.seek(0)
    dfs = pd.read_html(handle)
    df = dfs[0]
    df = df[df.columns.values.tolist()[:2]]
    year_ranges = df[df.columns.values.tolist()[1]].tolist()
    names = df[df.columns.values.tolist()[0]].tolist()
    name = None
    for count, year_range in enumerate(year_ranges):
        if "-" in year_range:
            start_year, end_year = [int(x) for x in year_range.split("-")]
        else:
            start_year = end_year = int(year_range)
        if start_year <= year >= end_year:
            name = names[count].strip()
            break
    if name is None:
        raise ValueError("name is null")
    coach_url = None
    soup = BeautifulSoup(html, "lxml")
    for a in soup.find_all("a", href=True):
        a_text = a.get_text().strip()
        if a_text == name:
            coach_url = urllib.parse.urljoin(url, a.get("href"))
            break
    if coach_url is None:
        raise ValueError("coach is null")
    o = urlparse(coach_url)
    last_component = o.path.split("/")[-1]
    identifier, _ = os.path.splitext(last_component)
    return CoachModel(
        identifier=identifier,
        name=name,
    )


@MEMORY.cache(ignore=["session"])
def _cached_create_afl_afltables_coach_model(
    url: str, session: requests_cache.CachedSession, year: int
) -> CoachModel:
    return _create_afl_afltables_coach_model(url, session, year)


def create_afl_afltables_coach_model(
    url: str, session: requests_cache.CachedSession, year: int
) -> CoachModel:
    """Create a coach model from AFL tables."""
    if not pytest_is_running.is_running():
        return _cached_create_afl_afltables_coach_model(url, session, year)
    with session.cache_disabled():
        return _create_afl_afltables_coach_model(url, session, year)
