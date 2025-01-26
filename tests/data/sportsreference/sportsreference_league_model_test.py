"""Tests for the sportsreference league model class."""
import unittest

import requests_cache
from sportsball.data.sportsreference.sportsreference_league_model import SportsReferenceLeagueModel
from sportsball.data.league import League


class TestSportsReferenceLeagueModel(unittest.TestCase):

    def setUp(self):
        self.session = requests_cache.CachedSession(backend="memory")
        self.league_model = SportsReferenceLeagueModel(self.session, League.NBA, "https://www.basketball-reference.com/boxscores/")

    def test_league(self):
        self.assertEqual(self.league_model.league, League.NBA)
