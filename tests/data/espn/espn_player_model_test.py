"""Tests for the ESPN player model class."""
import datetime
import os
import unittest

import requests_mock
import requests_cache
from sportsball.data.espn.espn_player_model import create_espn_player_model


class TestESPNPlayerModel(unittest.TestCase):

    def setUp(self):
        self._session = requests_cache.CachedSession(backend="memory")
        self.dir = os.path.dirname(__file__)

    def test_identifier(self):
        dt = datetime.datetime(2023, 9, 15, 0, 15)
        identifier = "a"
        with requests_mock.Mocker() as m:
            player_model = create_espn_player_model(
                self._session,
                {
                    "playerId": identifier,
                },
                dt,
            )

            self.assertEqual(player_model.identifier, identifier)
