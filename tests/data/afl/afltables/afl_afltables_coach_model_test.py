"""Tests for the afltables coach model class."""
import os
import unittest
import datetime

import requests_mock
import requests_cache
from sportsball.data.afl.afltables.afl_afltables_coach_model import create_afl_afltables_coach_model


class TestAFLTablesCoachModel(unittest.TestCase):

    def setUp(self):
        self._session = requests_cache.CachedSession(backend="memory")
        self.dir = os.path.dirname(__file__)

    def test_dt(self):
        with requests_mock.Mocker() as m:
            url = "https://afltables.com/afl/stats/coaches/goldcoast.html"
            with open(os.path.join(self.dir, "coaches_goldcoast.html"), "rb") as f:
                m.get(url, content=f.read())
            with open(os.path.join(self.dir, "Guy_McKenna.html"), "rb") as f:
                m.get("https://afltables.com/afl/stats/coaches/Guy_McKenna.html", content=f.read())
            coach_model = create_afl_afltables_coach_model(
                url=url,
                session=self._session,
                year=2012,
                dt=datetime.datetime(2012, 10, 10),
            )
            self.assertEqual(coach_model.name, "McKenna, Guy")
