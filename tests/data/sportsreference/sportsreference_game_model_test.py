"""Tests for the sportsreference game model class."""
import datetime
import os
import unittest

import requests_mock
import requests_cache
from sportsball.data.sportsreference.sportsreference_game_model import create_sportsreference_game_model
from sportsball.data.league import League


class TestSportsReferenceGameModel(unittest.TestCase):

    def setUp(self):
        self.session = requests_cache.CachedSession(backend="memory")
        self.dir = os.path.dirname(__file__)

    def test_dt(self):
        url = "https://www.basketball-reference.com/boxscores/202501230ATL.html"
        with requests_mock.Mocker() as m:
            with open(os.path.join(self.dir, "202501230ATL.html"), "rb") as f:
                m.get(url, content=f.read())
            m.get("https://historical-forecast-api.open-meteo.com/v1/forecast?latitude=33.757222&longitude=-84.396389&start_date=2025-01-22&end_date=2025-01-23&hourly=temperature_2m&hourly=relative_humidity_2m&hourly=dew_point_2m&hourly=apparent_temperature&hourly=precipitation&hourly=rain&hourly=snowfall&hourly=snow_depth&hourly=weather_code&hourly=pressure_msl&hourly=surface_pressure&hourly=cloud_cover&hourly=cloud_cover_low&hourly=cloud_cover_mid&hourly=cloud_cover_high&hourly=et0_fao_evapotranspiration&hourly=vapour_pressure_deficit&hourly=wind_speed_10m&hourly=wind_speed_100m&hourly=wind_direction_10m&hourly=wind_direction_100m&hourly=wind_gusts_10m&hourly=soil_temperature_0_to_7cm&hourly=soil_temperature_7_to_28cm&hourly=soil_temperature_28_to_100cm&hourly=soil_temperature_100_to_255cm&hourly=soil_moisture_0_to_7cm&hourly=soil_moisture_7_to_28cm&hourly=soil_moisture_28_to_100cm&hourly=soil_moisture_100_to_255cm&daily=weather_code&daily=temperature_2m_max&daily=temperature_2m_min&daily=temperature_2m_mean&daily=apparent_temperature_max&daily=apparent_temperature_min&daily=apparent_temperature_mean&daily=sunrise&daily=sunset&daily=daylight_duration&daily=sunshine_duration&daily=precipitation_sum&daily=rain_sum&daily=snowfall_sum&daily=precipitation_hours&daily=wind_speed_10m_max&daily=wind_gusts_10m_max&daily=wind_direction_10m_dominant&daily=shortwave_radiation_sum&daily=et0_fao_evapotranspiration&timezone=America%2FNew_York&format=flatbuffers")
            game_model = create_sportsreference_game_model(
                self.session,
                url,
                League.NBA,
                datetime.datetime(2010, 10, 10, 10, 10, 0),
            )
            self.assertEqual(game_model.dt, datetime.datetime(2025, 1, 23, 19, 30))

    def test_dt_old_style(self):
        url = "http://www.basketball-reference.com/boxscores/201606190GSW.html"
        with requests_mock.Mocker() as m:
            with open(os.path.join(self.dir, "201606190GSW.html"), "rb") as f:
                m.get(url, content=f.read())
            with open(os.path.join(self.dir, "2016.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/teams/CLE/2016.html", content=f.read())
            with open(os.path.join(self.dir, "shumpim01.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/s/shumpim01.html", content=f.read())
            with open(os.path.join(self.dir, "mcraejo01.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/m/mcraejo01.html", content=f.read())
            with open(os.path.join(self.dir, "jefferi01.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/j/jefferi01.html", content=f.read())
            with open(os.path.join(self.dir, "varejan01.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/v/varejan01.html", content=f.read())
            with open(os.path.join(self.dir, "loveke01.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/l/loveke01.html", content=f.read())
            with open(os.path.join(self.dir, "thomptr01.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/t/thomptr01.html", content=f.read())
            with open(os.path.join(self.dir, "curryst01.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/c/curryst01.html", content=f.read())
            with open(os.path.join(self.dir, "kaunsa01.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/k/kaunsa01.html", content=f.read())
            with open(os.path.join(self.dir, "jamesle01.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/j/jamesle01.html", content=f.read())
            with open(os.path.join(self.dir, "willima01.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/w/willima01.html", content=f.read())
            with open(os.path.join(self.dir, "irvinky01.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/i/irvinky01.html", content=f.read())
            with open(os.path.join(self.dir, "smithjr01.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/s/smithjr01.html", content=f.read())
            with open(os.path.join(self.dir, "GSW_2016.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/teams/GSW/2016.html", content=f.read())
            with open(os.path.join(self.dir, "greendr01.html"), "rb") as f:
                m.get("https://www.basketball-reference.com/players/g/greendr01.html", content=f.read())
            with open(os.path.join(self.dir, "barbole01.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/b/barbole01.html", content=f.read())
            with open(os.path.join(self.dir, "barneha02.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/b/barneha02.html", content=f.read())
            with open(os.path.join(self.dir, "thompkl01.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/t/thompkl01.html", content=f.read())
            with open(os.path.join(self.dir, "thompkl01.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/t/thompkl01.html", content=f.read())
            with open(os.path.join(self.dir, "ezelife01.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/e/ezelife01.html", content=f.read())
            with open(os.path.join(self.dir, "livinsh01.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/l/livinsh01.html", content=f.read())
            with open(os.path.join(self.dir, "greendr01.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/g/greendr01.html", content=f.read())
            with open(os.path.join(self.dir, "bogutan01.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/b/bogutan01.html", content=f.read())
            with open(os.path.join(self.dir, "looneke01.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/l/looneke01.html", content=f.read())
            with open(os.path.join(self.dir, "speigma01.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/s/speigma01.html", content=f.read())
            with open(os.path.join(self.dir, "iguodan01.html"), "rb") as f:
                m.get("http://www.basketball-reference.com/players/i/iguodan01.html", content=f.read())
            m.get("https://historical-forecast-api.open-meteo.com/v1/forecast?latitude=37.750278&longitude=-122.203056&start_date=2016-06-18&end_date=2016-06-19&hourly=temperature_2m&hourly=relative_humidity_2m&hourly=dew_point_2m&hourly=apparent_temperature&hourly=precipitation&hourly=rain&hourly=snowfall&hourly=snow_depth&hourly=weather_code&hourly=pressure_msl&hourly=surface_pressure&hourly=cloud_cover&hourly=cloud_cover_low&hourly=cloud_cover_mid&hourly=cloud_cover_high&hourly=et0_fao_evapotranspiration&hourly=vapour_pressure_deficit&hourly=wind_speed_10m&hourly=wind_speed_100m&hourly=wind_direction_10m&hourly=wind_direction_100m&hourly=wind_gusts_10m&hourly=soil_temperature_0_to_7cm&hourly=soil_temperature_7_to_28cm&hourly=soil_temperature_28_to_100cm&hourly=soil_temperature_100_to_255cm&hourly=soil_moisture_0_to_7cm&hourly=soil_moisture_7_to_28cm&hourly=soil_moisture_28_to_100cm&hourly=soil_moisture_100_to_255cm&daily=weather_code&daily=temperature_2m_max&daily=temperature_2m_min&daily=temperature_2m_mean&daily=apparent_temperature_max&daily=apparent_temperature_min&daily=apparent_temperature_mean&daily=sunrise&daily=sunset&daily=daylight_duration&daily=sunshine_duration&daily=precipitation_sum&daily=rain_sum&daily=snowfall_sum&daily=precipitation_hours&daily=wind_speed_10m_max&daily=wind_gusts_10m_max&daily=wind_direction_10m_dominant&daily=shortwave_radiation_sum&daily=et0_fao_evapotranspiration&timezone=America%2FLos_Angeles&format=flatbuffers")
            
            game_model = create_sportsreference_game_model(
                self.session,
                url,
                League.NBA,
                datetime.datetime(2010, 10, 10, 10, 10, 0),
            )
            self.assertEqual(game_model.dt, datetime.datetime(2016, 6, 19, 20, 0))
