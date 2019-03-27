"""Model representations of API interfaces"""

from dataclasses import dataclass

from termlink.configuration import Config
from termlink.client import Client

_client = Client()
_configuration = Config()
_logger = _configuration.logger


def _parse_id_from_location_header(res):
    """Parses the "id" from the HTTP "Location" header"""
    parts = res.headers["location"].split("/")
    return parts[-1]


@dataclass(frozen=True)
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

    @staticmethod
    def create(coding, project=_configuration.get_property('LO_PROJECT'), client=_client):
        """
        Creates a 'Coding'.

        Args:
            coding (:obj:`Coding`):     The `Coding` to create
            project (str)               A LifeOmic project
            client (:obj:`Client`):     A `Client` object

        Returns:
            The id of the created `Coding`
        """
        path = "/v1/terminology/projects/%s/codings" % project
        res = client.request('put', path=path, data=coding.to_json())
        _id = _parse_id_from_location_header(res)
        _logger.debug("Created 'Coding' with id '%s'" % _id)
        return _id

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

    @staticmethod
    def create(relationship, project=_configuration.get_property('LO_PROJECT'), client=_client):
        """
        Creates a 'Relationship'.

        Args:
            relationship (:obj:`Relationship`):     The `Relationship` to create
            project (str)               A LifeOmic project
            client (:obj:`Client`):     A `Client` object

        Returns:
            The id of the created `Relationship`
        """
        path = "/v1/terminology/projects/%s/relationships" % project
        res = client.request('put', path=path, data=relationship.to_json())
        _id = _parse_id_from_location_header(res)
        _logger.debug("Created 'Relationship' with id '%s'" % _id)
        return _id

    def to_json(self):
        """Converts :this: into a JSON object"""
        return {
            "equivalence": self.equivalence,
            "source": self.source,
            "target": self.target,
        }
