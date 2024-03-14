"""The prototype class for a team."""

# pylint: disable=too-many-arguments
from typing import Dict, Sequence

import pandas as pd

from .odds_model import OddsModel
from .player_model import PlayerModel


class TeamModel:
    """The prototype team class."""

    def __init__(
        self,
        identifier: str,
        name: str,
        location: str,
        players: Sequence[PlayerModel],
        odds: Dict[str, OddsModel],
    ) -> None:
        self._identifier = identifier
        self._name = name
        self._location = location
        self._players = players
        self._odds = odds

    @property
    def identifier(self) -> str:
        """Return the identifier."""
        return self._identifier

    @property
    def name(self) -> str:
        """Return the name."""
        return self._name

    @property
    def location(self) -> str:
        """Return the location."""
        return self._location

    @property
    def players(self) -> Sequence[PlayerModel]:
        """Return a list of players in the team."""
        return self._players

    @property
    def odds(self) -> Dict[str, OddsModel]:
        """Return the odds."""
        return self._odds

    def to_frame(self) -> pd.DataFrame:
        """Render the team as a dataframe."""
        data = {
            "identifier": [self.identifier],
            "name": [self.name],
            "location": [self.location],
        }

        for count, player in enumerate(self.players):
            player_df = player.to_frame()
            for column in player_df.columns.values:
                data[str(count) + "_" + column] = player_df[column].to_list()

        for k, v in self.odds.items():
            odds_df = v.to_frame()
            for column in odds_df.columns.values:
                data[k + "_" + column] = odds_df[column].to_list()

        return pd.DataFrame(data={"team_" + k: v for k, v in data.items()})
