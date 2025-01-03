"""NFL SportsDB team model."""

from ....cache import MEMORY
from ...team_model import TeamModel


@MEMORY.cache
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
