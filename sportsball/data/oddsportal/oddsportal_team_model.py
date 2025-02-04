"""Odds Portal team model."""

# pylint: disable=too-many-arguments,duplicate-code,line-too-long,too-many-locals
import base64
import datetime
import json

import pytest_is_running
import requests_cache
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.hashes import SHA256
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from ...cache import MEMORY
from ..google.google_news_model import create_google_news_models
from ..league import League
from ..team_model import TeamModel
from ..x.x_social_model import create_x_social_model
from .oddsportal_odds_model import create_oddsportal_odds_model


def _create_oddsportal_team_model(
    session: requests_cache.CachedSession,
    dt: datetime.datetime,
    team_name: str,
    league: League,
    points: float | None,
    version_id: str,
    sport_id: str,
    unique_id: str,
    default_bet_id: str,
    default_scope_id: str,
    xhash: str,
    salt: bytes,
    password: bytes,
    bookie_names: dict[str, str],
    team_idx: int,
) -> TeamModel:
    response = session.get(
        f"https://www.oddsportal.com/match-event/{version_id}-{sport_id}-{unique_id}-{default_bet_id}-{default_scope_id}-{xhash}.dat",
        headers={
            "X-Requested-With": "XMLHttpRequest",
        },
    )
    response.raise_for_status()
    decoded_data = base64.b64decode(response.content).decode()
    encrypted, key = decoded_data.split(":")
    encrypted_bytes = base64.urlsafe_b64decode(encrypted)
    key_bytes = bytes.fromhex(key)
    kdf = PBKDF2HMAC(
        algorithm=SHA256(),
        length=32,
        salt=salt,
        iterations=1000,
        backend=default_backend(),
    )
    aes_key = kdf.derive(password)
    cipher = Cipher(
        algorithms.AES(aes_key), modes.CBC(key_bytes), backend=default_backend()
    )
    decryptor = cipher.decryptor()
    decrypted_bytes = decryptor.update(encrypted_bytes) + decryptor.finalize()
    decrypted_data = decrypted_bytes.decode("utf-8")
    end_of_json = decrypted_data.rfind("}")
    if end_of_json != -1:
        decrypted_data = decrypted_data[: end_of_json + 1]
    parsed_data = json.loads(decrypted_data)
    try:
        odds_data = parsed_data["d"]["oddsdata"]["back"][
            f"E-{default_bet_id}-{default_scope_id}-0-0-0"
        ]
    except KeyError:
        back = parsed_data["d"]["oddsdata"]["back"]
        odds_data = back[sorted(list(back.keys()))[0]]
    try:
        outcome_id = odds_data["outcomeId"][team_idx]
    except KeyError:
        outcome_id = odds_data["outcomeId"][str(team_idx)]
    history = odds_data["history"][outcome_id]
    odds_models = []
    for bookie_id, bookie_name in bookie_names.items():
        for odds, _, timestamp in history.get(bookie_id, []):
            odds_models.append(
                create_oddsportal_odds_model(
                    odds,
                    datetime.datetime.fromtimestamp(timestamp),
                    bookie_name,
                    bookie_id,  # type: ignore
                )
            )

    return TeamModel(
        identifier=team_name,
        name=team_name,
        points=points,
        players=[],
        odds=odds_models,
        ladder_rank=None,
        location=None,
        news=create_google_news_models(team_name, session, dt, league),
        social=create_x_social_model(team_name, session, dt),
        field_goals=None,
    )


@MEMORY.cache(ignore=["session"])
def _cached_create_oddsportal_team_model(
    session: requests_cache.CachedSession,
    dt: datetime.datetime,
    team_name: str,
    league: League,
    points: float | None,
    version_id: str,
    sport_id: str,
    unique_id: str,
    default_bet_id: str,
    default_scope_id: str,
    xhash: str,
    salt: bytes,
    password: bytes,
    bookie_names: dict[str, str],
    team_idx: int,
) -> TeamModel:
    return _create_oddsportal_team_model(
        session,
        dt,
        team_name,
        league,
        points,
        version_id,
        sport_id,
        unique_id,
        default_bet_id,
        default_scope_id,
        xhash,
        salt,
        password,
        bookie_names,
        team_idx,
    )


def create_oddsportal_team_model(
    session: requests_cache.CachedSession,
    dt: datetime.datetime,
    team_name: str,
    league: League,
    points: float | None,
    version_id: str,
    sport_id: str,
    unique_id: str,
    default_bet_id: str,
    default_scope_id: str,
    xhash: str,
    salt: bytes,
    password: bytes,
    bookie_names: dict[str, str],
    team_idx: int,
) -> TeamModel:
    """Create a team model based off the odds portal response."""
    if not pytest_is_running.is_running() and dt < datetime.datetime.now().replace(
        tzinfo=dt.tzinfo
    ) - datetime.timedelta(days=7):
        return _cached_create_oddsportal_team_model(
            session,
            dt,
            team_name,
            league,
            points,
            version_id,
            sport_id,
            unique_id,
            default_bet_id,
            default_scope_id,
            xhash,
            salt,
            password,
            bookie_names,
            team_idx,
        )
    with session.cache_disabled():
        return _create_oddsportal_team_model(
            session,
            dt,
            team_name,
            league,
            points,
            version_id,
            sport_id,
            unique_id,
            default_bet_id,
            default_scope_id,
            xhash,
            salt,
            password,
            bookie_names,
            team_idx,
        )
