"""NFL Sports DB league model."""

from typing import Iterator

import requests

from ...game_model import GameModel
from ...league import League
from ...league_model import LeagueModel
from ...season_type import SeasonType
from .nfl_sportsdb_game_model import create_nfl_sportsdb_game_model


class NFLSportsDBLeagueModel(LeagueModel):
    """NFL SportsDB implementation of the league model."""

    # pylint: disable=too-many-arguments

    def __init__(self, session: requests.Session) -> None:
        super().__init__(League.NFL, session)

    def _produce_games(
        self,
        round_str: str,
        week: int,
        league_id: str,
        season_year: int,
        season_type: SeasonType,
    ) -> Iterator[GameModel]:
        # pylint: disable=line-too-long
        response = self.session.get(
            f"https://www.thesportsdb.com/api/v1/json/3/eventsround.php?id={league_id}&r={round_str}&s={season_year}"
        )
        response.raise_for_status()
        games = response.json()
        events = games["events"]
        if events is None:
            raise ValueError("events is null.")
        for count, game in enumerate(events):
            yield create_nfl_sportsdb_game_model(
                self.session,
                game,
                week,
                count,
                self.league,
                season_year,  # pyright: ignore
                season_type,
            )

    @property
    def games(self) -> Iterator[GameModel]:
        league_id = "4391"
        response = self.session.get(
            f"https://www.thesportsdb.com/api/v1/json/3/search_all_seasons.php?id={league_id}"
        )
        response.raise_for_status()
        seasons = response.json()
        for season in seasons["seasons"]:
            season_year = season["strSeason"]
            for season_type in SeasonType:
                match season_type:
                    case SeasonType.OFFSEASON:
                        return
                    case SeasonType.PRESEASON:
                        try:
                            yield from self._produce_games(
                                str(500), 0, league_id, season_year, season_type
                            )
                        except ValueError:
                            pass
                    case SeasonType.REGULAR:
                        try:
                            for count, round_str in enumerate(range(1, 125)):
                                yield from self._produce_games(
                                    str(round_str),
                                    count,
                                    league_id,
                                    season_year,
                                    season_type,
                                )
                        except ValueError:
                            pass
                    case SeasonType.POSTSEASON:
                        for count, round_str in enumerate(
                            [125, 150, 160, 170, 180, 200]
                        ):
                            try:
                                yield from self._produce_games(
                                    str(round_str),
                                    21 + count,
                                    league_id,
                                    season_year,
                                    season_type,
                                )
                            except ValueError:
                                pass
