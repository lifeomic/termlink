"""Utilities for building request sessions

This module is used to configure and create request sessions.
"""

import requests

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

_RETRIES = Retry(total=5, backoff_factor=1, status_forcelist=[403, 500, 502, 504])


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
