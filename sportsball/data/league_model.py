"""The prototype class defining how to interface to the league."""

# pylint: disable=line-too-long
from typing import Iterator, get_args, get_origin

import pandas as pd
import requests
import tqdm
from flatten_json import flatten  # type: ignore
from pydantic import BaseModel

from .field_type import FieldType
from .game_model import GAME_DT_COLUMN, GameModel
from .league import League
from .model import Model

LEAGUE_COLUMN = "league"
DELIMITER = "/"


class LeagueModel(Model):
    """The prototype league model class."""

    _df: pd.DataFrame | None

    def __init__(self, league: League, session: requests.Session) -> None:
        super().__init__(session)
        self._league = league
        self._df = None

    @property
    def games(self) -> Iterator[GameModel]:
        """Find all the games in this league."""
        raise NotImplementedError("games not implemented by LeagueModel parent class.")

    @property
    def league(self) -> League:
        """Return the league this league model represents."""
        return self._league

    def to_frame(self) -> pd.DataFrame:
        """Render the league as a dataframe."""
        df = self._df
        if df is None:
            dfs = [
                pd.DataFrame(flatten(x.model_dump(by_alias=True), DELIMITER))
                for x in tqdm.tqdm(self.games, desc="Games")
            ]
            if not dfs:
                return pd.DataFrame()
            df = pd.concat(dfs)

            def find_nested_paths(
                field_type: str, model_class: type[BaseModel]
            ) -> list[str]:
                nested_paths = []
                for field_name, field in model_class.model_fields.items():
                    nested_field_type = field.field_info.extra.get("type")  # type: ignore
                    if nested_field_type != field_type:
                        continue
                    if issubclass(
                        get_origin(field.annotation) or field.annotation,  # type: ignore
                        BaseModel,  # type: ignore
                    ):
                        nested_paths.extend(
                            [
                                DELIMITER.join([field_name, x])
                                for x in find_nested_paths(field_type, field.annotation)  # type: ignore
                            ]
                        )
                    elif get_origin(field.annotation) == list and issubclass(
                        get_args(field.annotation)[0], BaseModel
                    ):
                        for i in range(1000):
                            nested_paths.extend(
                                [
                                    DELIMITER.join([field_name, str(i), x])
                                    for x in find_nested_paths(
                                        field_type, get_args(field.annotation)[0]
                                    )
                                ]
                            )
                return nested_paths

            df.attrs[FieldType.LOOKAHEAD] = list(
                set(df.columns.values)
                & set(find_nested_paths(FieldType.LOOKAHEAD, GameModel))
            )
            df.attrs[FieldType.ODDS] = list(
                set(df.columns.values)
                & set(find_nested_paths(FieldType.ODDS, GameModel))
            )
            df.attrs[FieldType.POINTS] = list(
                set(df.columns.values)
                & set(find_nested_paths(FieldType.POINTS, GameModel))
            )
            df.attrs[FieldType.TEXT] = list(
                set(df.columns.values)
                & set(find_nested_paths(FieldType.TEXT, GameModel))
            )
            df.attrs[FieldType.CATEGORICAL] = list(
                set(df.columns.values)
                & set(find_nested_paths(FieldType.CATEGORICAL, GameModel))
            )

            for categorical_column in df.attrs[FieldType.CATEGORICAL]:
                df[categorical_column] = df[categorical_column].astype("category")
            df[GAME_DT_COLUMN] = pd.to_datetime(df[GAME_DT_COLUMN], utc=True)
            df = df.sort_values(
                by=GAME_DT_COLUMN,
                ascending=True,
            )

            self._df = df
        return df
