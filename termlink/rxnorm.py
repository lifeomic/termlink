"""Uploads RxNorm files.

This module provides methods to extract, transform and load relationships
defined by the RxNorm dataset.

The download files for RxNorm are provided at https://www.nlm.nih.gov/research/umls/rxnorm/.
"""
import csv
import json
import os

from urllib.parse import urlparse

from termlink.commands import SubCommand
from termlink.configuration import Config
from termlink.models import Coding, Relationship
from termlink.services import RelationshipService

configuration = Config()
logger = configuration.logger

_RXCONSO_PATH = "rrf/RXNCONSO.rrf"
_RXCONSO_FIELDS = [
    "RXCUI",
    "LAT",
    "TS",
    "LUI",
    "STT",
    "SUI",
    "ISPREF",
    "RXAUI",
    "SAUI",
    "SCUI",
    "SDUI",
    "SAB",
    "TTY",
    "CODE",
    "STR",
    "SRL",
    "SUPPRESS",
    "CVF",
]

_RXNREL_PATH = "rrf/RXNREL.rrf"
_RXNREL_FIELDS = [
    "RXCUI1",
    "RXAUI1",
    "STYPE1",
    "REL",
    "RXCUI2",
    "RXAUI2",
    "STYPE2",
    "RELA",
    "RUI",
    "SRUI",
    "SAB",
    "SL",
    "DIR",
    "RG",
    "SUPPRESS",
    "CVF",
]


def _to_equivalence(rel):
    """Converts a RxNorm relationship code into an equivalence"""
    switch = {"RB": "subsumes", "RN": "specializes", "RO": "relatedto"}
    return switch[rel]


def get_relationships(uri):
    """Converts the RxNorm file set into `Relationship`s"""

    if uri.scheme != 'file':
        raise ValueError("'uri.scheme' %s not supported" % uri.scheme)

    root = uri.path

    concepts_and_atoms_and_codings = []
    path = os.path.join(root, _RXCONSO_PATH)
    logger.info("Loading data from '%s'.", path)
    with open(path, "r") as f:
        reader = csv.DictReader(f, delimiter="|", fieldnames=_RXCONSO_FIELDS)
        for row in reader:

            # Skip all vocabularies except RxNorm
            if row["SAB"] != "RXNORM":
                continue

            concept = row["RXCUI"]
            atom = row["RXAUI"]
            coding = Coding(
                system="http://www.nlm.nih.gov/research/umls/rxnorm",
                code=row["CODE"],
                display=row["STR"],
            )
            concepts_and_atoms_and_codings.append((concept, atom, coding))

    codings = [coding for concept, atom,
               coding in concepts_and_atoms_and_codings]

    concepts_id = {}
    atoms_id = {}
    for idx, coding in enumerate(codings):
        (concept, atom, coding) = concepts_and_atoms_and_codings[idx]
        concepts_id[concept] = coding
        atoms_id[atom] = coding

    # TODO - Add support for ATOM to ATOM relationships for MMSL and VANDF
    relationships = []
    path = os.path.join(root, _RXNREL_PATH)
    logger.info("Loading data from '%s'.", path)
    with open(path, "r") as f:
        reader = csv.DictReader(f, delimiter="|", fieldnames=_RXNREL_FIELDS)
        for row in reader:

            # Skip all non RB relationships
            if row["REL"] != "RB":
                continue

            # Skip if source is missing
            if row["RXCUI1"] not in concepts_id:
                continue

            # Skip if target is missing
            if row["RXCUI2"] not in concepts_id:
                continue

            equivalence = _to_equivalence(row["REL"])
            source = concepts_id[row["RXCUI1"]]
            target = concepts_id[row["RXCUI2"]]

            relationship = Relationship(equivalence, source, target)
            relationships.append(relationship)

    return relationships


class Command(SubCommand):
    """
    A `SubCommand` for RxNorm operations
    """

    @staticmethod
    def execute(args):
        """
        Prints a JSON array of `Relationship` objects to stdout

        Args:
            args: `argparse` parsed arguments
            stdout: output stream (default: `sys.stdout`)
        """
        uri = urlparse(args.uri)
        service = Service(uri)
        relationships = service.get_relationships()
        dumped = Relationship.schema().dump(relationships, many=True)
        print(json.dumps(dumped))


class Service(RelationshipService):
    """Converts the RxNorm database"""

    def __init__(self, uri):
        """
        Bootstraps a service

        Args:
            uri: URI to root location of .rrf files
        """

        if uri.scheme != 'file':
            raise ValueError("'uri.scheme' %s not supported" % uri.scheme)

        self.uri = uri

    def get_relationships(self):
        """
        Parses a list of `Relationship` objects.
        """
        return get_relationships(self.uri)
