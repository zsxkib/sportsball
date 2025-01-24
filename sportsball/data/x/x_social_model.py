"""X social model."""

import datetime
import logging
import os

import pytest_is_running
import requests
import requests_cache
import tweepy  # type: ignore
from dateutil import parser

from ...cache import MEMORY
from ..social_model import SocialModel

X_TEAM_IDENTIFIER_MAP: dict[str, str] = {}
X_API_KEY = "X_API_KEY"
X_API_SECRET_KEY = "X_API_SECRET_KEY"
X_ACCESS_TOKEN = "X_ACCESS_TOKEN"
X_ACCESS_TOKEN_SECRET = "X_ACCESS_TOKEN_SECRET"


def _create_x_social_model(
    identifier: str,
    session: requests.Session,
    dt: datetime.datetime,
) -> list[SocialModel]:
    api_key = os.environ.get(X_API_KEY)
    api_secret_key = os.environ.get(X_API_SECRET_KEY)
    access_token = os.environ.get(X_ACCESS_TOKEN)
    access_token_secret = os.environ.get(X_ACCESS_TOKEN_SECRET)
    if (
        api_key is None
        or api_secret_key is None
        or access_token is None
        or access_token_secret is None
    ):
        return []

    username = X_TEAM_IDENTIFIER_MAP.get(identifier)
    if username is None:
        logging.warning("Team identifier %s X handle not found.", identifier)
        return []

    auth = tweepy.OAuth1UserHandler(
        api_key, api_secret_key, access_token, access_token_secret
    )
    api = tweepy.API(auth)
    api.session = session

    end_dt = dt - datetime.timedelta(days=1)
    start_dt = dt - datetime.timedelta(days=1)

    social_media = []
    for status in tweepy.Cursor(
        api.user_timeline, screen_name=username, tweet_mode="extended"
    ).items():
        # Filter by date range
        if start_dt <= status.created_at <= end_dt:
            social_media.append(
                SocialModel(
                    network="X",
                    post=status["text"],
                    comments=status["reply_count"],
                    reposts=status["retweet_count"],
                    likes=status["favorite_count"],
                    views=None,
                    published=parser.parse(status["created_at"]),
                )
            )
    return sorted(social_media, key=lambda x: x.published)


@MEMORY.cache(ignore=["session"])
def _cached_create_x_social_model(
    identifier: str,
    session: requests.Session,
    dt: datetime.datetime,
) -> list[SocialModel]:
    return _create_x_social_model(identifier, session, dt)


def create_x_social_model(
    identifier: str,
    session: requests_cache.CachedSession,
    dt: datetime.datetime,
) -> list[SocialModel]:
    """Create social models from X."""
    if (
        not pytest_is_running.is_running()
        and dt < datetime.datetime.now() - datetime.timedelta(days=7)
    ):
        return _cached_create_x_social_model(identifier, session, dt)
    with session.cache_disabled():
        return _create_x_social_model(identifier, session, dt)
