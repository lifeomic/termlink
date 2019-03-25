"""Model and utility methods for 'Relationship' objects.

This module defines the 'Relationship' @dataclass and provides utility methods
for managing objects via the API.
"""
from dataclasses import dataclass
from urllib.parse import urljoin

import grequests

from termlink import configuration, sessions
from termlink.batches import batch as _batch
from termlink.configuration import logger

_URL = configuration.get_url()
_PATH = "/v1/terminology/projects/%s/relationships" % configuration.get_project()
_ENDPOINT = urljoin(_URL, _PATH)
_HEADERS = configuration.get_auth_headers()
_SESSION = sessions.get_session()


def _build_request(relationship):
    """
    Builds a PUT request from a :Relationship:.
    """
    return grequests.put(
        _ENDPOINT, headers=_HEADERS, json=relationship.to_json(), session=_SESSION
    )


def _parse_id(res):
    """
    Parses the 'id' from the responses 'location' header.
    """
    if res is None:
        logger.warning("Failed to create 'Relationship'")
        return None

    if res.status_code != 201:
        print(res)
        raise Exception("Failed to create 'Relationship'")

    parts = res.headers["location"].split("/")
    return parts[-1]


def create(relationships, batch_size=10, sleep=0):
    """
    Uploads a collection of :Relationship: values via the REST API.
    """
    _ids = []
    for batch in _batch(relationships, batch_size, sleep):
        requests = [_build_request(relationship) for relationship in batch]
        responses = grequests.map(requests, size=batch_size)
        _ids.extend([_parse_id(res) for res in responses])

    return _ids


@dataclass
class Relationship:
    """
    A 'Relationship' object as defined by the API.

    Attributes:
        equivalence (str):  The degree of equivalence between concepts.
        source (str):       The source concept.
        target (str):       The target concept.
    """
    equivalence: str
    source: str
    target: str

    def to_json(self):
        """Converts :this: into a JSON object"""
        return {
            "equivalence": self.equivalence,
            "source": self.source,
            "target": self.target,
        }
