"""A session that rotates proxies."""

# pylint: disable=W0223,too-many-boolean-expressions
import datetime
import logging
import os
import random

import numpy as np
import requests
import requests_cache
import urllib3
from func_timeout import FunctionTimedOut, func_set_timeout  # type: ignore
from random_user_agent.params import OperatingSystem  # type: ignore
from random_user_agent.params import SoftwareName
from random_user_agent.user_agent import UserAgent  # type: ignore
from tenacity import (after_log, before_log, retry, retry_if_exception_type,
                      stop_after_attempt)

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

    def request(self, method, url, *args, **kwargs):  # pyright: ignore
        return self._perform_proxy_request(method, url, *args, **kwargs)
