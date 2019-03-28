"""Model representations of API interfaces"""

from dataclasses import asdict, dataclass

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
    system: str = None
    version: str = None
    code: str = None
    display: str = None

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
        return {k : v for k, v in asdict(self).items() if v is not None}


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
        return {k : v for k, v in asdict(self).items() if v is not None}
