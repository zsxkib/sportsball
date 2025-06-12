"""A session that rotates proxies."""

# pylint: disable=W0223,too-many-boolean-expressions,protected-access,unused-argument,too-many-arguments
import datetime
import logging
import os
import random
import re
import sqlite3
import urllib.parse
from contextlib import contextmanager
from io import BytesIO
from typing import Any, MutableMapping, Optional

import numpy as np
import requests
import requests_cache
import urllib3
import wayback  # type: ignore
from func_timeout import FunctionTimedOut, func_set_timeout  # type: ignore
from random_user_agent.params import OperatingSystem  # type: ignore
from random_user_agent.params import SoftwareName
from random_user_agent.user_agent import UserAgent  # type: ignore
from requests import PreparedRequest
from requests.cookies import RequestsCookieJar
from requests.models import Request, Response
from requests_cache import AnyResponse, ExpirationTime
from tenacity import (after_log, before_log, retry, retry_if_exception_type,
                      stop_after_attempt, wait_random_exponential)
from urllib3.response import HTTPResponse

from .session import DEFAULT_TIMEOUT

FAST_FAIL_DOMAINS = [
    "https://news.google.com/",
    "https://historical-forecast-api.open-meteo.com/",
    "https://api.open-meteo.com/",
]


def _is_fast_fail_url(url: str | None) -> bool:
    if url is None:
        return False
    for fast_fail_domain in FAST_FAIL_DOMAINS:
        if url.startswith(fast_fail_domain):
            return True
    return False


def _redirect_to(response: requests.Response) -> str | None:
    redirect_url = None
    for line in response.text.splitlines():
        if "window.location.href" in line and "==" not in line:
            match = re.search(r'window\.location\.href\s*=\s*["\'](.*?)["\']', line)
            if match:
                redirect_url = match.group(1)
                url_split = line.split(redirect_url)
                if len(url_split) >= 2:
                    post_url_line = url_split[-1]
                    if "+" in post_url_line:
                        redirect_url = None
                        continue
                redirect_url = urllib.parse.urljoin(response.url, redirect_url)
                logging.info("Following %s", redirect_url)
                break
    return redirect_url


class ProxySession(requests_cache.CachedSession):
    """A requests session that can rotate between different proxies."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._proxies = []
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        self._last_fetched = None
        software_names = [SoftwareName.CHROME.value]
        operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]
        self._user_agent_rotator = UserAgent(
            software_names=software_names, operating_systems=operating_systems
        )
        self._wayback_client = wayback.WaybackClient()
        self._wayback_disabled = False

    def _suggest_proxy(self) -> str:
        proxies = self._proxies
        if (
            not proxies
            or self._last_fetched is None
            or (
                self._last_fetched
                < datetime.datetime.now() - datetime.timedelta(minutes=30)
            )
        ):
            proxies = [""]  # This indicates that no proxy is used
            proxies_txt = os.environ.get("PROXIES")
            if proxies_txt is not None:
                proxies.extend(proxies_txt.split(","))
            random.shuffle(proxies)
            self._proxies = proxies
            self._last_fetched = datetime.datetime.now()

        proxy = random.choices(
            population=proxies,
            weights=np.linspace(1.0, 0.0, len(proxies)).tolist(),
            k=1,
        )
        return proxy[0]

    def _wayback_machine_request(
        self, method, url, **kwargs
    ) -> requests.Response | None:
        if method.upper() != "GET":
            return None
        try:
            for record in self._wayback_client.search(url, fast_latest=True):
                if record.timestamp.replace(
                    tzinfo=None
                ) < datetime.datetime.now().replace(tzinfo=None) - datetime.timedelta(
                    days=350 * 10
                ):
                    continue
                with self._wayback_client.get_memento(record) as memento:
                    cookies = RequestsCookieJar()
                    response = Response()
                    response.status_code = memento.status_code
                    response._content = memento.content
                    response.url = url
                    response.headers = memento.headers
                    response.cookies = cookies
                    response.raw = HTTPResponse(
                        body=BytesIO(memento.content),
                        status=memento.status_code,
                        headers=memento.headers,
                        preload_content=False,
                    )

                    request = Request(
                        method=method,
                        url=url,
                        headers=kwargs.get("headers"),
                        cookies=cookies,
                    )
                    prepared_request = request.prepare()
                    prepared_request.prepare_cookies(cookies)
                    response.request = prepared_request

                    return response
        except (
            wayback.exceptions.MementoPlaybackError,  # pyright: ignore
            requests.exceptions.ChunkedEncodingError,
            requests.exceptions.ContentDecodingError,
        ):  # pyright: ignore
            pass
        return None

    def _create_fixed_response(self, original_response: Response) -> Response:
        """Create a new response with corrected Content-Length header to fix server gzip/header mismatch."""
        from requests.models import Response as RequestsResponse
        from requests import PreparedRequest
        from urllib3.response import HTTPResponse
        from io import BytesIO
        
        # Create a new response object
        fixed_response = RequestsResponse()
        
        # Copy basic attributes
        fixed_response.status_code = original_response.status_code
        fixed_response.reason = getattr(original_response, 'reason', 'OK')
        fixed_response.url = original_response.url
        fixed_response.headers = original_response.headers.copy()
        fixed_response.cookies = original_response.cookies
        fixed_response.encoding = original_response.encoding
        fixed_response.history = getattr(original_response, 'history', [])
        
        # Fix the Content-Length header to match actual content
        content = original_response.content
        fixed_response.headers['Content-Length'] = str(len(content))
        fixed_response._content = content
        
        # Create a proper request object if missing
        if original_response.request is None:
            prepared_request = PreparedRequest()
            prepared_request.method = 'GET'
            prepared_request.url = original_response.url
            prepared_request.headers = {}
            fixed_response.request = prepared_request
        else:
            fixed_response.request = original_response.request
        
        # Create a proper raw response for caching
        fixed_response.raw = HTTPResponse(
            body=BytesIO(content),
            status=original_response.status_code,
            headers=fixed_response.headers,
            preload_content=False,
            original_response=getattr(original_response.raw, 'original_response', None)
        )
        
        return fixed_response

    @func_set_timeout(DEFAULT_TIMEOUT)
    def _perform_timeout_send(
        self, request: requests.PreparedRequest, no_wayback: bool, **kwargs
    ) -> Any:
        key = self.cache.create_key(request)

        if not self.settings.disabled:
            # Check the cache
            cached_response = self.cache.get_response(key)
            if cached_response:
                return cached_response

            logging.info(
                "Request for %s not cached (no-wayback: %s).",
                request.url,
                str(no_wayback),
            )

            # Otherwise check the wayback machine
            if not _is_fast_fail_url(request.url) and not no_wayback:
                response = self._wayback_machine_request(
                    request.method, request.url, headers=request.headers
                )
                if response is not None and response.ok:
                    logging.info(
                        "Found wayback machine memento for URL: %s", request.url
                    )
                    try:
                        self.cache.save_response(response=response, cache_key=key)
                    except urllib3.exceptions.IncompleteRead as e:
                        logging.warning(
                            "Failed to cache wayback response for %s due to server Content-Length/gzip mismatch: %s. "
                            "Content retrieved successfully (%d bytes), but caching skipped due to server bug.",
                            request.url,
                            str(e),
                            len(response.content)
                        )
                        # Try to cache by creating a properly constructed response with fixed headers
                        try:
                            fixed_response = self._create_fixed_response(response)
                            self.cache.save_response(response=fixed_response, cache_key=key)
                            logging.info("Successfully cached wayback response with corrected Content-Length header.")
                        except Exception as cache_fix_error:
                            logging.warning("Could not cache wayback response even with header fix: %s", cache_fix_error)
                    return response
        else:
            logging.info("Request for %s caching disabled.", request.url)

        try:
            response = super().send(request, **kwargs)
        except urllib3.exceptions.IncompleteRead as e:
            logging.warning(
                "IncompleteRead during request for %s due to server Content-Length/gzip mismatch: %s. "
                "Retrying request without caching to get content.",
                request.url,
                str(e)
            )
            # Disable caching and retry
            old_disabled = self.settings.disabled
            self.settings.disabled = True
            try:
                response = super().send(request, **kwargs)
                logging.info("Successfully retrieved content (%d bytes) without caching.", len(response.content))
            finally:
                self.settings.disabled = old_disabled
        
        if not _is_fast_fail_url(response.url):
            response.raise_for_status()
        return response

    @retry(
        stop=stop_after_attempt(64),
        after=after_log(logging.getLogger(__name__), logging.DEBUG),
        before=before_log(logging.getLogger(__name__), logging.DEBUG),
        wait=wait_random_exponential(multiplier=1, max=240),
        retry=retry_if_exception_type(FunctionTimedOut)
        | retry_if_exception_type(requests.exceptions.ProxyError)
        | retry_if_exception_type(requests.exceptions.ConnectionError)
        | retry_if_exception_type(requests.exceptions.ChunkedEncodingError)
        | retry_if_exception_type(ValueError)
        | retry_if_exception_type(requests.exceptions.HTTPError)
        | retry_if_exception_type(requests.exceptions.ReadTimeout)
        | retry_if_exception_type(sqlite3.OperationalError),
        reraise=True,
    )
    def _perform_retry_send(
        self, request: requests.PreparedRequest, no_wayback: bool, **kwargs
    ) -> Any:
        return self._perform_timeout_send(request, no_wayback, **kwargs)

    def send(
        self,
        request: PreparedRequest,
        expire_after: ExpirationTime = None,  # pyright: ignore
        only_if_cached: bool = False,
        refresh: bool = False,
        force_refresh: bool = False,
        **kwargs,
    ) -> AnyResponse:
        if _is_fast_fail_url(request.url):
            response = super().send(
                request,
                expire_after=expire_after,
                only_if_cached=only_if_cached,
                refresh=refresh,
                force_refresh=force_refresh,
                **kwargs,
            )
            try:
                self.cache.save_response(response)
            except urllib3.exceptions.IncompleteRead as e:
                logging.warning(
                    "Failed to cache fast-fail response for %s due to server Content-Length/gzip mismatch: %s. "
                    "Content retrieved successfully (%d bytes), but caching skipped due to server bug.",
                    request.url,
                    str(e),
                    len(response.content)
                )
                # Try to cache by creating a properly constructed response with fixed headers
                try:
                    fixed_response = self._create_fixed_response(response)
                    self.cache.save_response(fixed_response)
                    logging.info("Successfully cached fast-fail response with corrected Content-Length header.")
                except Exception as cache_fix_error:
                    logging.warning("Could not cache fast-fail response even with header fix: %s", cache_fix_error)
            return response

        return self._perform_retry_send(
            request,
            self._wayback_disabled,
            expire_after=expire_after,
            only_if_cached=only_if_cached,
            refresh=refresh,
            force_refresh=force_refresh,
            **kwargs,
        )

    def request(  # type: ignore
        self,
        method: str,
        url: str,
        *args,
        headers: Optional[MutableMapping[str, str]] = None,
        expire_after: ExpirationTime = None,  # pyright: ignore
        only_if_cached: bool = False,
        refresh: bool = False,
        force_refresh: bool = False,
        **kwargs,
    ) -> AnyResponse:
        if "timeout" not in kwargs:
            if _is_fast_fail_url(url):
                kwargs["timeout"] = 5.0
            else:
                kwargs["timeout"] = DEFAULT_TIMEOUT
        if headers is None:
            headers = {}
        if "User-Agent" not in headers:
            headers["User-Agent"] = (
                self._user_agent_rotator.get_random_user_agent().strip()
            )
        proxy = self._suggest_proxy()
        if proxy:
            logging.debug("Using proxy: %s", proxy)
            kwargs.setdefault(
                "proxies",
                {
                    "http": proxy,
                    "https": proxy,
                },
            )
        response = super().request(
            method,
            url,
            *args,
            headers=headers,
            expire_after=expire_after,
            only_if_cached=only_if_cached,
            refresh=refresh,
            force_refresh=force_refresh,
            **kwargs,
        )
        redirects = 0
        while (redirect_url := _redirect_to(response)) is not None:
            response = super().request(
                method,
                redirect_url,
                *args,
                headers=headers,
                expire_after=expire_after,
                only_if_cached=only_if_cached,
                refresh=refresh,
                force_refresh=force_refresh,
                **kwargs,
            )
            redirects += 1
            if redirects >= 10:
                break

        return response

    @contextmanager
    def wayback_disabled(self):
        """Disable lookups on the wayback machine."""
        old_state = self._wayback_disabled
        self._wayback_disabled = True
        try:
            yield
        finally:
            self._wayback_disabled = old_state


def create_proxy_session() -> ProxySession:
    """Creates a standard proxy session."""
    return ProxySession(
        "sportsball",
        expire_after=requests_cache.NEVER_EXPIRE,
        allowable_methods=("GET", "HEAD", "POST"),
        stale_if_error=True,
    )
