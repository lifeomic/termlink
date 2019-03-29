"""Uploads RxNorm files.

This module provides methods to extract, transform and load relationships
defined by the RxNorm dataset.

The download files for RxNorm are provided at https://www.nlm.nih.gov/research/umls/rxnorm/.
"""
import csv
import os

from termlink.configuration import Config
from termlink.models import Coding, Relationship

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
    """Converts a relationship into an equivalence"""
    switch = {"RB": "subsumes", "RN": "specializes", "RO": "relatedto"}
    return switch[rel]


def upload(root):
    """Uploads the RxNorm dataset"""
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
                "http://www.nlm.nih.gov/research/umls/rxnorm",
                None,
                row["CODE"],
                row["STR"],
            )
            concepts_and_atoms_and_codings.append((concept, atom, coding))

    codings = [coding for concept, atom, coding in concepts_and_atoms_and_codings]
    _ids = [Coding.create(coding) for coding in codings]

    concepts_id = {}
    atoms_id = {}
    for idx, coding in enumerate(codings):
        # If a requests fails then the _id is None and needs to be skipped
        if _ids[idx] is not None:
            (concept, atom, coding) = concepts_and_atoms_and_codings[idx]
            concepts_id[concept] = _ids[idx]
            atoms_id[atom] = _ids[idx]

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

    [Relationship.create(relationship) for relationship in relationships]
