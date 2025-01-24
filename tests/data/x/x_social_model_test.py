"""Tests for the X social model class."""
import datetime
import unittest

import requests_cache

from sportsball.data.x.x_social_model import create_x_social_model


class TestXSocialModel(unittest.TestCase):

    def setUp(self):
        self._session = requests_cache.CachedSession(backend="memory")
        self._social_models = create_x_social_model("", self._session, datetime.datetime(2010, 10, 10, 10, 10, 10))

    def test_empty(self):
        self.assertListEqual(self._social_models, [])
