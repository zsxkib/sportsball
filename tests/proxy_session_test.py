"""Tests for the proxy session class."""
import datetime
import http
import unittest
from unittest.mock import MagicMock

from sportsball.proxy_session import ProxySession
import wayback


class TestProxySession(unittest.TestCase):

    def setUp(self):
        self.session = ProxySession()

    def test_wayback(self):
        url = "https://www.thing.com"
        timestamp = int(datetime.datetime.now().timestamp())
        status_code = http.HTTPStatus.OK
        wayback_client = wayback.WaybackClient()
        record = wayback.CdxRecord(
            "",
            timestamp,
            url,
            "",
            status_code,
            "",
            0,
            "https://web.archive.org/web/19961231235847id_/http://www.nasa.gov/",
            "https://web.archive.org/web/19961231235847/http://www.nasa.gov/",
        )
        memento = wayback.Memento(
            url=url,
            timestamp=timestamp,
            mode=wayback.Mode.original,
            memento_url="",
            status_code=status_code,
            headers={},
            encoding="utf8",
            raw=None,
            raw_headers={},
            links=[],
            history=[],
            debug_history=[],
        )
        wayback_client.search = MagicMock(return_value=[record])
        wayback_client.get_memento = MagicMock(return_value=memento)
        response = self.session.get(url)
        self.assertTrue(response.ok)
