"""Tests for the afltables game model class."""
import unittest
import os

import requests_cache
import requests_mock
from sportsball.data.afl.afltables.afl_afltables_game_model import _create_afl_afltables_game_model
from sportsball.data.league import League


class TestAFLTablesGameModel(unittest.TestCase):

    def setUp(self):
        self._session = requests_cache.CachedSession(backend="memory")
        self.dir = os.path.dirname(__file__)

    def test_player_identifier(self):
        url = "https://afltables.com/afl/stats/games/2025/081820250330.html"
        with requests_mock.Mocker() as m:
            with open(os.path.join(self.dir, "081820250330.html"), "rb") as f:
                m.get(url, content=f.read())
            with open(os.path.join(self.dir, "perth.html"), "rb") as f:
                m.get("https://afltables.com/afl/venues/perth.html", content=f.read())
            with open(os.path.join(self.dir, "westcoast_idx.html"), "rb") as f:
                m.get("https://afltables.com/afl/teams/westcoast_idx.html", content=f.read())
            with open(os.path.join(self.dir, "fremantle_idx.html"), "rb") as f:
                m.get("https://afltables.com/afl/teams/fremantle_idx.html", content=f.read())
            m.get("https://historical-forecast-api.open-meteo.com/v1/forecast?latitude=-31.9511597&longitude=115.884175&start_date=2025-03-29&end_date=2025-03-30&hourly=temperature_2m&hourly=relative_humidity_2m&hourly=dew_point_2m&hourly=apparent_temperature&hourly=precipitation&hourly=rain&hourly=snowfall&hourly=snow_depth&hourly=weather_code&hourly=pressure_msl&hourly=surface_pressure&hourly=cloud_cover&hourly=cloud_cover_low&hourly=cloud_cover_mid&hourly=cloud_cover_high&hourly=et0_fao_evapotranspiration&hourly=vapour_pressure_deficit&hourly=wind_speed_10m&hourly=wind_speed_100m&hourly=wind_direction_10m&hourly=wind_direction_100m&hourly=wind_gusts_10m&hourly=soil_temperature_0_to_7cm&hourly=soil_temperature_7_to_28cm&hourly=soil_temperature_28_to_100cm&hourly=soil_temperature_100_to_255cm&hourly=soil_moisture_0_to_7cm&hourly=soil_moisture_7_to_28cm&hourly=soil_moisture_28_to_100cm&hourly=soil_moisture_100_to_255cm&daily=weather_code&daily=temperature_2m_max&daily=temperature_2m_min&daily=temperature_2m_mean&daily=apparent_temperature_max&daily=apparent_temperature_min&daily=apparent_temperature_mean&daily=sunrise&daily=sunset&daily=daylight_duration&daily=sunshine_duration&daily=precipitation_sum&daily=rain_sum&daily=snowfall_sum&daily=precipitation_hours&daily=wind_speed_10m_max&daily=wind_gusts_10m_max&daily=wind_direction_10m_dominant&daily=shortwave_radiation_sum&daily=et0_fao_evapotranspiration&timezone=Australia%2FPerth&format=flatbuffers")

            game_model = _create_afl_afltables_game_model(
                0,
                self._session,
                url,
                2,
                {},
                League.AFL,
                2025,
                season_type=None,
            )
            self.assertIsNotNone(game_model.teams[0].players[0].identifier)
