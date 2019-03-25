"""Model and utility methods for 'Coding' objects.

This module defines the 'Coding' @dataclass and provides utility methods for
managing objects via the API.
"""
from dataclasses import dataclass
from urllib.parse import urljoin

import grequests

from termlink import configuration, sessions
from termlink.batches import batch as _batch
from termlink.configuration import logger

_URL = configuration.get_url()
_PATH = "/v1/terminology/projects/%s/codings" % configuration.get_project()
_ENDPOINT = urljoin(_URL, _PATH)
_HEADERS = configuration.get_auth_headers()
_SESSION = sessions.get_session()


def _build_request(coding):
    """
    Builds a PUT request from a :Coding:.
    """
    return grequests.put(
        _ENDPOINT, headers=_HEADERS, json=coding.to_json(), session=_SESSION
    )


def _parse_id(res):
    """
    Parses the 'id' from the responses 'location' header.
    """
    if res is None:
        logger.warning("Failed to create 'Coding'")
        return None

    if res.status_code != 201:
        print(res)
        raise Exception("Failed to create 'Coding'")

    parts = res.headers["location"].split("/")
    return parts[-1]


def upload(codings, batch_size=10, sleep=0):
    """
    Uploads a collection of :Coding: values via the REST API.
    """
    _ids = []
    for batch in _batch(codings, batch_size, sleep):
        requests = [_build_request(coding) for coding in batch]
        responses = grequests.map(requests, size=batch_size)
        _ids.extend([_parse_id(res) for res in responses])

    return _ids


@dataclass
class Coding:
    """
    A 'Coding' object as defined by the API.

    Attributes:
        system (str):   Identity of the terminology system
        version (str):  Version of the system
        code (str):     Symbol in syntax defined by the system
        display (str):  Representation defined by the system
    """
    system: str
    version: str
    code: str
    display: str

    def to_json(self):
        """Converts :this: into a JSON object"""
        o = {}

        if self.system is not None:
            o["system"] = self.system

        if self.version is not None:
            o["version"] = self.version

        if self.code is not None:
            o["code"] = self.code

        if self.display is not None:
            o["display"] = self.display

        return o
