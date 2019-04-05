"""Model representations of API interfaces"""

from dataclasses import asdict, dataclass
from dataclasses_json import DataClassJsonMixin

from termlink.configuration import Config

_configuration = Config()
_logger = _configuration.logger


@dataclass(frozen=True)
class Coding(DataClassJsonMixin):
    """
    A 'Coding' object as defined by the API.

    Attributes:
        system (str):   Identity of the terminology system
        version (str):  Version of the system
        code (str):     Symbol in syntax defined by the system
        display (str):  Representation defined by the system
    """
    type: str = 'coding'
    system: str = None
    version: str = None
    code: str = None
    display: str = None


@dataclass
class Relationship(DataClassJsonMixin):
    """
    A 'Relationship' object as defined by the API.

    Attributes:
        equivalence (str):  The degree of equivalence between concepts.
        source object:       The source concept.
        target object:       The target concept.
    """
    equivalence: str
    source: Coding
    target: Coding
