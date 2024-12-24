"""NFL SportsDB team model."""

from ...team_model import TeamModel


def create_nfl_sportsdb_team_model(team_id: str, name: str, points: float) -> TeamModel:
    """Create a team model based off the sportsdb NFL response."""
    return TeamModel(
        identifier=team_id,
        name=name,
        points=points,
        players=[],
        odds=[],
        ladder_rank=None,
        location=None,
    )
