"""Combined league model."""

# pylint: disable=raise-missing-from,too-many-locals
import logging
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Iterator

from scrapesession.scrapesession import ScrapeSession  # type: ignore
from pydantic import ValidationError

from ..game_model import GameModel
from ..league import League
from ..league_model import LeagueModel
from .combined_game_model import create_combined_game_model


def _produce_league_games(league_model: LeagueModel) -> list[dict[str, Any]]:
    return [x.model_dump() for x in league_model.games]


class CombinedLeagueModel(LeagueModel):
    """The class implementing the combined league model."""

    def __init__(
        self,
        session: ScrapeSession,
        league: League,
        league_models: list[LeagueModel],
        league_filter: str | None,
    ) -> None:
        super().__init__(league, session)
        if league_filter is not None:
            league_models = [x for x in league_models if x.name() == league_filter]
        if not league_models:
            raise ValueError("No league models to run")
        self._league_models = league_models

    @classmethod
    def team_identity_map(cls) -> dict[str, str]:
        """A map to resolve the different teams identities to a consistent identity."""
        raise NotImplementedError(
            "team_identity_map not implemented on CombinedLeagueModel parent class."
        )

    @classmethod
    def venue_identity_map(cls) -> dict[str, str]:
        """A map to resolve the different venue identities to a consistent identity."""
        raise NotImplementedError(
            "venue_identity_map not implemented on CombinedLeagueModel parent class."
        )

    @classmethod
    def player_identity_map(cls) -> dict[str, str]:
        """A map to resolve the different player identities to a consistent identity."""
        return {}

    @property
    def games(self) -> Iterator[GameModel]:
        games: dict[str, list[GameModel]] = {}
        team_identity_map = self.team_identity_map()
        for league_model in self._league_models:
            league_model.clear_session()
        with ThreadPoolExecutor(
            min(multiprocessing.cpu_count(), len(self._league_models))
        ) as p:
            # We want to terminate immediately if any of our runners runs into trouble.

            futures = {
                p.submit(_produce_league_games, model): model
                for model in self._league_models
            }

            results = []
            try:
                for future in as_completed(futures):
                    result = future.result()  # Raises if an exception occurred
                    results.append(result)
            except Exception:
                # Cancel all pending futures
                for f in futures:
                    f.cancel()
                raise  # Optionally re-raise the exception
        def validate_game_with_defaults(game_data):
            """Validate game data with fallback for missing fields."""
            try:
                return GameModel.model_validate(game_data)
            except ValidationError as e:
                error_str = str(e)
                
                # Handle common missing field issues
                if "venue.address.altitude" in error_str:
                    # Set default altitude if missing
                    if game_data.get("venue", {}).get("address") is not None:
                        game_data["venue"]["address"].setdefault("altitude", None)
                        
                elif "venue.address.weather" in error_str:
                    # Handle missing weather fields
                    venue = game_data.get("venue", {})
                    address = venue.get("address", {})
                    weather = address.get("weather", {})
                    
                    if weather is not None:
                        # Set defaults for all missing weather fields
                        weather_defaults = {
                            "dew_point": None, "apparent_temperature": None, "precipitation_probability": None,
                            "precipitation": None, "rain": None, "showers": None, "snowfall": None,
                            "snow_depth": None, "weather_code": None, "sealevel_pressure": None,
                            "surface_pressure": None, "cloud_cover_total": None, "cloud_cover_low": None,
                            "cloud_cover_mid": None, "cloud_cover_high": None, "visibility": None,
                            "evapotranspiration": None, "reference_evapotranspiration": None,
                            "vapour_pressure_deficit": None, "wind_speed_10m": None, "wind_speed_80m": None,
                            "wind_speed_120m": None, "wind_speed_180m": None, "wind_direction_10m": None,
                            "wind_direction_80m": None, "wind_direction_120m": None, "wind_direction_180m": None,
                            "wind_gusts": None, "temperature_80m": None, "temperature_120m": None,
                            "temperature_180m": None, "soil_temperature_0cm": None, "soil_temperature_6cm": None,
                            "soil_temperature_18cm": None, "soil_temperature_54cm": None, "soil_moisture_0cm": None,
                            "soil_moisture_1cm": None, "soil_moisture_3cm": None, "soil_moisture_9cm": None,
                            "soil_moisture_27cm": None, "daily_weather_code": None, "daily_maximum_temperature_2m": None,
                            "daily_minimum_temperature_2m": None, "daily_maximum_apparent_temperature_2m": None,
                            "daily_minimum_apparent_temperature_2m": None, "sunrise": None, "sunset": None,
                            "daylight_duration": None, "sunshine_duration": None, "uv_index": None,
                            "uv_index_clear_sky": None, "rain_sum": None, "showers_sum": None,
                            "snowfall_sum": None, "precipitation_sum": None, "precipitation_hours": None,
                            "precipitation_probability_max": None, "maximum_wind_speed_10m": None,
                            "maximum_wind_gusts_10m": None, "dominant_wind_direction": None,
                            "shortwave_radiation_sum": None, "daily_reference_evapotranspiration": None
                        }
                        for field, default in weather_defaults.items():
                            weather.setdefault(field, default)
                
                # Try validation again after setting defaults
                try:
                    return GameModel.model_validate(game_data)
                except ValidationError:
                    # If still failing, log and skip this game
                    logging.warning("Skipping game due to validation errors: %s", str(e)[:200])
                    return None
                    
            return None
        
        game_lists = [[validate_game_with_defaults(y) for y in x] for x in results]
        # Filter out None values (skipped games)
        game_lists = [[game for game in game_list if game is not None] for game_list in game_lists]

        for game_list in game_lists:
            for game_model in game_list:
                game_components = [str(game_model.dt.date())]
                for team in game_model.teams:
                    if team.identifier not in team_identity_map:
                        logging.warning(
                            "%s for team %s not found in team identity map.",
                            team.identifier,
                            team.name,
                        )
                    team_identifier = team_identity_map.get(
                        team.identifier, team.identifier
                    )
                    game_components.append(team_identifier)
                game_components = sorted(game_components)
                key = "-".join(game_components)
                games[key] = games.get(key, []) + [game_model]
        names: dict[str, str] = {}
        coach_names: dict[str, str] = {}
        player_ffill: dict[str, dict[str, Any]] = {}
        team_ffill: dict[str, dict[str, Any]] = {}
        coach_ffill: dict[str, dict[str, Any]] = {}
        last_game_number = None
        for game_models in games.values():
            game_model = create_combined_game_model(  # type: ignore
                game_models=game_models,
                venue_identity_map=self.venue_identity_map(),
                team_identity_map=team_identity_map,
                player_identity_map=self.player_identity_map(),
                session=self.session,
                names=names,
                coach_names=coach_names,
                last_game_number=last_game_number,
                player_ffill=player_ffill,
                team_ffill=team_ffill,
                coach_ffill=coach_ffill,
            )
            last_game_number = game_model.game_number
            yield game_model
