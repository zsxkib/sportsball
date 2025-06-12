"""Tests for the proxy session class."""
import datetime
import http
import unittest
from unittest.mock import MagicMock, patch

import requests
import urllib3.exceptions
import wayback.exceptions

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

    def test_wayback_raises_exception(self):
        url = "https://www.thing.com"

        def search_exception(*args, **kwargs):
            raise wayback.exceptions.MementoPlaybackError()

        wayback_client = wayback.WaybackClient()
        wayback_client.search = search_exception
        self.session._wayback_client = wayback_client
        response = self.session.get(url)
        self.assertTrue(response.ok)

    def test_create_fixed_response(self):
        """Test that _create_fixed_response properly fixes Content-Length headers."""
        # Create a response with mismatched Content-Length header
        original_response = requests.Response()
        original_response.status_code = 200
        original_response.url = "https://afltables.com/afl/stats/coaches/Dani_Laidley.html"
        original_response.headers = {"Content-Length": "10681", "Content-Type": "text/html"}
        original_response._content = b"x" * 96203  # Actual content size

        # Mock a proper request object
        original_response.request = requests.PreparedRequest()
        original_response.request.method = "GET"
        original_response.request.url = original_response.url

        # Apply the fix
        fixed_response = self.session._create_fixed_response(original_response)

        # Verify the fix
        self.assertEqual(fixed_response.status_code, 200)
        self.assertEqual(fixed_response.url, original_response.url)
        self.assertEqual(fixed_response.content, original_response.content)
        self.assertEqual(fixed_response.headers["Content-Length"], "96203")
        self.assertIsNotNone(fixed_response.request)
        self.assertIsNotNone(fixed_response.raw)

    def test_dani_laidley_content_length_mismatch(self):
        """Test that the problematic Dani Laidley URL works with Content-Length/gzip fixes.
        
        This is an integration test for the specific server bug that caused pipeline crashes.
        AFL Tables server sends gzipped content with incorrect Content-Length headers.
        """
        url = "https://afltables.com/afl/stats/coaches/Dani_Laidley.html"
        
        try:
            response = self.session.get(url)
            
            # Verify successful response
            self.assertEqual(response.status_code, 200)
            self.assertGreater(len(response.content), 90000)  # Should be ~96K bytes
            
            # Verify it contains expected AFL coaching data
            content = response.text.lower()
            self.assertIn("dani laidley", content)
            self.assertTrue(
                "north melbourne" in content or "kangaroos" in content,
                "Should contain team information"
            )
            
        except Exception as e:
            self.fail(f"Dani Laidley URL should work with Content-Length fixes: {e}")

    def test_create_fixed_response_handles_missing_request(self):
        """Test that _create_fixed_response handles responses with missing request objects."""
        # Create a response without a request object (can happen with wayback responses)
        original_response = requests.Response()
        original_response.status_code = 200
        original_response.url = "https://afltables.com/test.html"
        original_response.headers = {"Content-Length": "50"}
        original_response._content = b"x" * 1000  # Content larger than reported
        original_response.request = None  # Missing request

        # Apply the fix
        fixed_response = self.session._create_fixed_response(original_response)

        # Verify the fix created a proper request object
        self.assertIsNotNone(fixed_response.request)
        self.assertEqual(fixed_response.request.method, "GET")
        self.assertEqual(fixed_response.request.url, original_response.url)
        self.assertEqual(fixed_response.headers["Content-Length"], "1000")
