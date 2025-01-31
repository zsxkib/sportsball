"""Tests for the combined player model class."""
import os
import unittest

import requests_mock
import requests_cache
from sportsball.data.combined.combined_player_model import create_combined_player_model
from sportsball.data.player_model import PlayerModel


class TestCombinedPlayerModel(unittest.TestCase):

    def setUp(self):
        self._session = requests_cache.CachedSession(backend="memory")
        self.dir = os.path.dirname(__file__)

    def test_field_goals_attempted(self):
        identifier = "a"
        field_goals_attempted = 10
        with requests_mock.Mocker() as m:
            player_model = PlayerModel(
                identifier="a",
                jersey="35",
                kicks=None,
                fumbles=None,
                fumbles_lost=None,
                field_goals=None,
                field_goals_attempted=field_goals_attempted,
                offensive_rebounds=None,
                assists=None,
                turnovers=None,
            )
            combined_player_model = create_combined_player_model(
                [player_model],
                identifier,
            )
            self.assertEqual(combined_player_model.field_goals_attempted, field_goals_attempted)
