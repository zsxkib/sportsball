"""NBA API team model."""

import pandas as pd

from ....cache import MEMORY
from ...team_model import TeamModel


@MEMORY.cache
def create_nba_nba_team_model(row: pd.Series, home: bool) -> TeamModel | None:
    """Create a team model from NBA API."""
    suffix = "_A" if home else "_B"
    # game_rotation = gamerotation.GameRotation(game_id=row["GAME_ID"])
    # player_dict = {}
    # for _, gr_row in game_rotation.get_data_frames()[int(home)].iterrows():
    #     player_dict[gr_row["PERSON_ID"]] = gr_row
    identifier = row["TEAM_ID" + suffix]
    if identifier is None:
        return None
    return TeamModel(
        identifier=str(identifier),
        name=row["TEAM_NAME" + suffix],
        players=[  # type: ignore
            # create_nba_nba_player_model(v, player_index) for v in player_dict.values()
        ],
        odds=[],
        points=float(row["PTS" + suffix]),
        ladder_rank=None,
        location=None,
    )
