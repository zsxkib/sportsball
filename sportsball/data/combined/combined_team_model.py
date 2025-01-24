"""Combined team model."""

# pylint: disable=too-many-locals
from ..news_model import NewsModel
from ..odds_model import OddsModel
from ..player_model import PlayerModel
from ..social_model import SocialModel
from ..team_model import TeamModel
from .combined_player_model import create_combined_player_model


def create_combined_team_model(
    team_models: list[TeamModel],
    identifier: str,
) -> TeamModel:
    """Create a team model by combining many team models."""
    location = None
    players: dict[str, list[PlayerModel]] = {}
    odds: dict[str, list[OddsModel]] = {}
    news: dict[str, NewsModel] = {}
    social: dict[str, SocialModel] = {}
    points = None
    ladder_rank = None
    field_goals = None
    for team_model in team_models:
        team_model_location = team_model.location
        if team_model_location is not None:
            location = team_model_location
        for player_model in team_model.players:
            key = player_model.jersey
            if key is None:
                key = player_model.identifier
            players[key] = players.get(key, []) + [player_model]
        for odds_model in team_model.odds:
            key = f"{odds_model.bookie.identifier}-{odds_model.odds}"
            odds[key] = odds.get(key, []) + [odds_model]
        team_model_points = team_model.points
        if team_model_points is not None:
            points = team_model_points
        team_model_ladder_rank = team_model.ladder_rank
        if team_model_ladder_rank is not None:
            ladder_rank = team_model_ladder_rank
        for news_model in team_model.news:
            news_key = "-".join(
                [
                    news_model.title,
                    str(news_model.published),
                    news_model.summary,
                    news_model.source,
                ]
            )
            news[news_key] = news_model
        for social_model in team_model.social:
            social_key = "-".join(
                [social_model.network, social_model.post, str(social_model.published)]
            )
            social[social_key] = social_model
        team_model_field_goals = team_model.field_goals
        if team_model_field_goals is not None:
            field_goals = team_model_field_goals

    return TeamModel(
        identifier=identifier,
        name=team_models[0].name,
        location=location,
        players=[  # pyright: ignore
            create_combined_player_model(x, x[0].identifier) for x in players.values()
        ],
        odds=[x[0] for x in odds.values()],
        points=points,
        ladder_rank=ladder_rank,
        news=sorted(news.values(), key=lambda x: x.published),
        social=sorted(social.values(), key=lambda x: x.published),
        field_goals=field_goals,
    )
