"""Tests for the HKJC HKJC player model class."""
import os
import unittest

import requests_mock
import requests_cache
from sportsball.data.hkjc.hkjc.hkjc_hkjc_player_model import create_hkjc_hkjc_player_model


class TestHKJCHKJCPlayerModel(unittest.TestCase):

    def setUp(self):
        self._session = requests_cache.CachedSession(backend="memory")
        self.dir = os.path.dirname(__file__)

    def test_no_table_for_sire(self):
        with requests_mock.Mocker() as m:
            url = "https://racing.hkjc.com/racing/information/english/Horse/SameSire.aspx?HorseSire=Nyquist"
            with open(os.path.join(self.dir, "sire_nyquist_2.html"), "rb") as f:
                m.get(url, content=f.read())
            player_model = create_hkjc_hkjc_player_model(
                session=self._session,
                url=url,
                jersey=None,
                handicap_weight=None,
                starting_position=None,
                weight=None,
            )
            self.assertEqual(player_model.name, "Nyquist")
