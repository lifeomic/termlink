"""Utilities for building request sessions

This module is used to configure and create request sessions.
"""

import requests

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from termlink.configuration import Config

configuration = Config()

_RETRIES = Retry(
    total=5,
    backoff_factor=1,
    status_forcelist=[
        403,
        500,
        502,
        504])


def get_session(pool_connections=10, pool_maxsize=10):
    """Creates a requests object"""
    session = requests.Session()
    session.mount(
        "http://",
        HTTPAdapter(
            pool_connections=pool_connections,
            pool_maxsize=pool_maxsize,
            max_retries=_RETRIES,
        ),
    )
    session.mount(
        "https://",
        HTTPAdapter(
            pool_connections=pool_connections,
            pool_maxsize=pool_maxsize,
            max_retries=_RETRIES,
        ),
    )
    return session


class Session(requests.Session):
    """An extended :class`<requests.Session>`.

    This session provides helper methods for interacting with the LifeOmic
    API.
    """

    def setup_authorization(self, account, api_key):
        """Sets HTTP headers for API authentication.

        Args:
            account (str):  a valid account
            api_key (str):  a valid API key
        """

        self.headers.update({
            "Authorization": "Bearer %s" % api_key,
            "LifeOmic-Account": account
        })
