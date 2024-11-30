"""Tests for the NFL ESPN game model."""
import unittest
import os
import json

import requests_cache

from sportsball.data.nfl.espn.nfl_espn_game_model import NFLESPNGameModel


class TestNFLESPNGameModel(unittest.TestCase):

    def setUp(self):
        self._session = requests_cache.CachedSession(backend="memory")
        with open(os.path.join(os.path.dirname(__file__), "event.json")) as handle:
            event_dict = json.load(handle)
            self._model = NFLESPNGameModel(event_dict, 1, 1, self._session)

    def test_to_frame(self):
        df = self._model.to_frame()
        self.assertIsNotNone(df)

    def test_attendance(self):
        attendance = self._model.attendance
        self.assertEqual(attendance, 33069)
