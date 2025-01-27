"""A session that rotates proxies."""

# pylint: disable=W0223,too-many-boolean-expressions,protected-access,unused-argument
import datetime
import logging
import os
import random
from io import BytesIO

import numpy as np
import requests
import requests_cache
import urllib3
import wayback  # type: ignore
from func_timeout import FunctionTimedOut, func_set_timeout  # type: ignore
from random_user_agent.params import OperatingSystem  # type: ignore
from random_user_agent.params import SoftwareName
from random_user_agent.user_agent import UserAgent  # type: ignore
from requests.cookies import RequestsCookieJar
from requests.models import Request, Response
from tenacity import (after_log, before_log, retry, retry_if_exception_type,
                      stop_after_attempt)
from urllib3.response import HTTPResponse

from .session import DEFAULT_TIMEOUT


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

    @func_set_timeout(DEFAULT_TIMEOUT)
    def _perform_request(self, *args, **kwargs) -> requests.Response:
        return super().request(*args, **kwargs)

    @retry(
        stop=stop_after_attempt(50),
        after=after_log(logging.getLogger(__name__), logging.DEBUG),
        before=before_log(logging.getLogger(__name__), logging.DEBUG),
        retry=retry_if_exception_type(FunctionTimedOut)
        | retry_if_exception_type(requests.exceptions.ProxyError)
        | retry_if_exception_type(requests.exceptions.ConnectionError)
        | retry_if_exception_type(requests.exceptions.ChunkedEncodingError)
        | retry_if_exception_type(ValueError)
        | retry_if_exception_type(requests.exceptions.HTTPError)
        | retry_if_exception_type(requests.exceptions.ReadTimeout),
    )
    def _perform_proxy_request(self, *args, **kwargs) -> requests.Response:
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
        kwargs.setdefault("timeout", DEFAULT_TIMEOUT)
        kwargs.setdefault("verify", False)
        if "headers" not in kwargs:
            kwargs["headers"] = {}
        kwargs["headers"]["User-Agent"] = (
            self._user_agent_rotator.get_random_user_agent()
        )

        try:
            response = self._perform_request(*args, **kwargs)
            response.raise_for_status()
            if not response.from_cache:  # pyright: ignore
                self._proxies.remove(proxy)
                self._proxies.insert(0, proxy)
            return response
        except Exception as e:
            logging.debug("Burning proxy: %s due to %s", proxy, str(e))
            self._proxies.remove(proxy)
            self._proxies.append(proxy)
            raise e

    def _wayback_machine_request(
        self, method, url, *args, **kwargs
    ) -> requests.Response | None:
        if method.upper() != "GET":
            return None
        try:
            for record in self._wayback_client.search(url, fast_latest=True):
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
        except wayback.exceptions.MementoPlaybackError:  # pyright: ignore
            pass
        return None

    def request(self, method, url, *args, **kwargs):  # pyright: ignore
        if not self.settings.disabled:
            # Check the cache
            cached_response = self.cache.get_response(url)
            if cached_response:
                return cached_response

            logging.info("Request for %s not cached.", url)

            # Otherwise check the wayback machine
            response = self._wayback_machine_request(method, url, *args, **kwargs)
            if response is not None and response.ok:
                logging.info("Found wayback machine memento for URL: %s", url)
                self.cache.save_response(response=response)
                return response

        response = self._perform_proxy_request(method, url, *args, **kwargs)

        if response.url.startswith("https://news.google.com/"):
            self.cache.save_response(response)

        return response
