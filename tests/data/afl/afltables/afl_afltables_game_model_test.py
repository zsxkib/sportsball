"""Tests for the afltables game model class."""
import os
import unittest
from unittest.mock import patch

import requests_cache
import requests_mock
import openmeteo_requests

from sportsball.data.afl.afltables.afl_afltables_game_model import AFLAFLTablesGameModel
from sportsball.data.game_model import GAME_ATTENDANCE_COLUMN, GAME_COLUMN_PREFIX
from sportsball.data.team_model import TEAM_COLUMN_PREFIX
from sportsball.data.player_model import PLAYER_COLUMN_PREFIX, PLAYER_KICKS_COLUMN
from sportsball.data.columns import COLUMN_SEPARATOR


class TestAFLAFLTablesGameModel(unittest.TestCase):

    def setUp(self):
        self._url = "https://afltables.com/afl/stats/games/2024/111620240307.html"
        self._session = requests_cache.CachedSession(backend="memory")
        self._model = AFLAFLTablesGameModel(
            self._url,
            self._session,
            1,
            0,
            None,
        )

    @patch.object(openmeteo_requests.Client, "weather_api")
    def test_attendance(self, mock_weather_api):
        mock_weather_api.return_value = []
        with requests_mock.Mocker() as m:
            with open(os.path.join(os.path.dirname(__file__), "game_model_test.html")) as handle:
                m.get(self._url, text=handle.read())
            with open(os.path.join(os.path.dirname(__file__), "scg_venue.html")) as handle:
                m.get("https://afltables.com/afl/venues/scg.html", text=handle.read())
            with open(os.path.join(os.path.dirname(__file__), "swans_team.html")) as handle:
                m.get("https://afltables.com/afl/teams/swans_idx.html", text=handle.read())
            with open(os.path.join(os.path.dirname(__file__), "melbourne_team.html")) as handle:
                m.get("https://afltables.com/afl/teams/melbourne_idx.html", text=handle.read())
            df = self._model.to_frame()
            attendance = df[COLUMN_SEPARATOR.join([GAME_COLUMN_PREFIX, GAME_ATTENDANCE_COLUMN])].values.tolist()[0]
            self.assertEqual(attendance, 40012)

    @patch.object(openmeteo_requests.Client, "weather_api")
    def test_kicks(self, mock_weather_api):
        mock_weather_api.return_value = []
        with requests_mock.Mocker() as m:
            with open(os.path.join(os.path.dirname(__file__), "game_model_test.html")) as handle:
                m.get(self._url, text=handle.read())
            with open(os.path.join(os.path.dirname(__file__), "scg_venue.html")) as handle:
                m.get("https://afltables.com/afl/venues/scg.html", text=handle.read())
            with open(os.path.join(os.path.dirname(__file__), "swans_team.html")) as handle:
                m.get("https://afltables.com/afl/teams/swans_idx.html", text=handle.read())
            with open(os.path.join(os.path.dirname(__file__), "melbourne_team.html")) as handle:
                m.get("https://afltables.com/afl/teams/melbourne_idx.html", text=handle.read())
            df = self._model.to_frame()
            kicks = df[COLUMN_SEPARATOR.join([GAME_COLUMN_PREFIX, str(0), TEAM_COLUMN_PREFIX, str(0), PLAYER_COLUMN_PREFIX, PLAYER_KICKS_COLUMN])].values.tolist()[0]
            self.assertEqual(kicks, 3)

    @patch.object(openmeteo_requests.Client, "weather_api")
    def test_no_attendance(self, mock_weather_api):
        mock_weather_api.return_value = []
        url = "https://afltables.com/afl/stats/games/1897/041518970508.html"
        model = AFLAFLTablesGameModel(
            url,
            self._session,
            1,
            0,
            None,
        )
        with requests_mock.Mocker() as m:
            with open(os.path.join(os.path.dirname(__file__), "game_model_no_attendance_test.html")) as handle:
                m.get(url, text=handle.read())
            with open(os.path.join(os.path.dirname(__file__), "victoria_park.html")) as handle:
                m.get("https://afltables.com/afl/venues/victoria_park.html", text=handle.read())
            with open(os.path.join(os.path.dirname(__file__), "collingwood_team.html")) as handle:
                m.get("https://afltables.com/afl/teams/collingwood_idx.html", text=handle.read())
            with open(os.path.join(os.path.dirname(__file__), "stkilda_team.html")) as handle:
                m.get("https://afltables.com/afl/teams/stkilda_idx.html", text=handle.read())
            df = model.to_frame()
            self.assertNotIn(COLUMN_SEPARATOR.join([GAME_COLUMN_PREFIX, GAME_ATTENDANCE_COLUMN]), df.columns.values)
