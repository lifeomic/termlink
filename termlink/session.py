"""Utilities for building request sessions

This module is used to configure and create request sessions.
"""

import requests

from termlink.configuration import Config

configuration = Config()

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
