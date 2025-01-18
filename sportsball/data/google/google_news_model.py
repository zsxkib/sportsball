"""Google news model."""

import datetime

import requests
from bs4 import BeautifulSoup
from dateutil import parser
from pygooglenews import GoogleNews  # type: ignore

from ...cache import MEMORY
from ..league import League, long_name
from ..news_model import NewsModel


@MEMORY.cache(ignore=["session"])
def create_google_news_models(
    query: str,
    session: requests.Session,
    dt: datetime.datetime,
    league: League,
) -> list[NewsModel]:
    """Create news models from google."""
    gn = GoogleNews(session=session)
    to_dt = dt - datetime.timedelta(days=1)
    from_dt = to_dt - datetime.timedelta(days=1)
    search_query = f'"{query}" + (sport OR {league} OR "{long_name(league)}")'
    s = gn.search(query=search_query, from_=str(from_dt), to_=str(to_dt))
    return sorted(
        [
            NewsModel(
                title=x["title"],
                published=parser.parse(x["published"]),
                summary=BeautifulSoup(x["summary"], features="lxml").get_text(),
                source=x["source"]["title"],
            )
            for x in s["entries"]
        ],
        key=lambda x: x.published,
    )
