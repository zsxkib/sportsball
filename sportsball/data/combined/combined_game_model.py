"""Combined game model."""

# pylint: disable=too-many-locals,line-too-long
import logging

import requests

from ..game_model import GameModel
from ..team_model import TeamModel
from ..venue_model import VenueModel
from .combined_team_model import create_combined_team_model
from .combined_venue_model import create_combined_venue_model


def _venue_models(
    game_models: list[GameModel], venue_identity_map: dict[str, str]
) -> tuple[list[VenueModel], str | None]:
    venue_models = []
    full_venue_identity = None
    for game_model in game_models:
        game_model_venue = game_model.venue
        if game_model_venue is not None:
            venue_identity = venue_identity_map.get(game_model_venue.identifier)
            if venue_identity is None:
                logging.warning(
                    "Failed to find %s venue identifier.", game_model_venue.identifier
                )
            else:
                full_venue_identity = venue_identity
            venue_models.append(game_model_venue)
    return venue_models, full_venue_identity


def _team_models(
    game_models: list[GameModel],
    team_identity_map: dict[str, str],
) -> list[TeamModel]:
    team_models: dict[str, list[TeamModel]] = {}
    for game_model in game_models:
        game_model_teams = game_model.teams
        if game_model_teams:
            for team_model in game_model_teams:
                team_identity = team_identity_map.get(team_model.identifier)
                if team_identity is None:
                    logging.warning(
                        "Failed to find %s team identifier.", team_model.identifier
                    )
                    team_identity = team_model.identifier
                team_models[team_identity] = team_models.get(team_identity, []) + [
                    team_model
                ]
    return [
        create_combined_team_model(v, k)  # pyright: ignore
        for k, v in team_models.items()
    ]


def create_combined_game_model(
    game_models: list[GameModel],
    venue_identity_map: dict[str, str],
    team_identity_map: dict[str, str],
    session: requests.Session,
) -> GameModel:
    """Create a game model by combining many game models."""
    venue_models, full_venue_identity = _venue_models(game_models, venue_identity_map)
    full_team_models = _team_models(game_models, team_identity_map)
    attendance = None
    end_dt = None
    year = None
    season_type = None
    week = None
    game_number = None
    postponed = None
    play_off = None
    for game_model in game_models:
        game_model_attendance = game_model.attendance
        if game_model_attendance is not None:
            attendance = game_model_attendance
        game_model_end_dt = game_model.end_dt
        if game_model_end_dt is not None:
            end_dt = game_model_end_dt
        game_model_year = game_model.year
        if game_model_year is not None:
            year = game_model_year
        game_model_season_type = game_model.season_type
        if game_model_season_type is not None:
            season_type = game_model_season_type
        game_model_week = game_model.week
        if game_model_week is not None:
            week = game_model_week
        game_model_game_number = game_model.game_number
        if game_model_game_number is not None:
            game_number = game_model_game_number
        game_model_postponed = game_model.postponed
        if game_model_postponed is not None:
            postponed = game_model_postponed
        game_model_play_off = game_model.play_off
        if game_model_play_off is not None:
            play_off = game_model_play_off

    if full_venue_identity is None and venue_models:
        for venue_model in venue_models:
            venue_model_identifier = venue_model.identifier
            if venue_model_identifier is not None:
                full_venue_identity = venue_model_identifier

    return GameModel(
        dt=game_models[0].dt,
        week=week,
        game_number=game_number,
        venue=create_combined_venue_model(venue_models, full_venue_identity, session),  # pyright: ignore
        teams=full_team_models,
        end_dt=end_dt,
        attendance=attendance,
        league=str(game_models[0].league),
        year=year,
        season_type=season_type,
        postponed=postponed,
        play_off=play_off,
    )
