"""Handles RxNorm conversion.

This module provides methods to extract, transform and load relationships
defined by the RxNorm dataset.

The download files for RxNorm are provided at https://www.nlm.nih.gov/research/umls/rxnorm/.
"""
import os
import json

from urllib.parse import urlparse

import petl as etl

from termlink.commands import SubCommand
from termlink.models import Coding, Relationship, RelationshipSchema
from termlink.services import RelationshipService

_RXNCONSO_FIELDS = ["RXCUI", "LAT", "TS", "LUI", "STT", "SUI", "ISPREF", "RXAUI",
                    "SAUI", "SCUI", "SDUI", "SAB", "TTY", "CODE", "STR", "SRL", "SUPPRESS", "CVF", ]
_RXNREL_FIELDS = ["RXCUI1", "RXAUI1", "STYPE1", "REL", "RXCUI2", "RXAUI2",
                  "STYPE2", "RELA", "RUI", "SRUI", "SAB", "SL", "DIR", "RG", "SUPPRESS", "CVF", ]


def _to_json(rec):
    """
    Convert record in table to Relationship as a JSON object

    Record is expected to have the following fields: [ source.CODE, source.STR, 
    target.CODE, target.STR]

    Args:
        rec: A table record

    Returns:
        A new record containing a single field, which is the JSON object
    """

    source = Coding(
        system="http://www.nlm.nih.gov/research/umls/rxnorm",
        code=rec['source.CODE'],
        display=rec['source.STR']
    )

    target = Coding(
        system="http://www.nlm.nih.gov/research/umls/rxnorm",
        code=rec['target.CODE'],
        display=rec['target.STR']
    )

    relationship = Relationship('subsumes', source, target)

    schema = RelationshipSchema()
    return [json.dumps(schema.dump(relationship))]


class Command(SubCommand):
    """
    A command executor for RxNorm operations
    """

    @staticmethod
    def execute(args):
        """
        Prints a JSON array of `Relationship` objects to stdout

        Args:
            args: `argparse` parsed arguments
        """
        uri = urlparse(args.uri)
        service = Service(uri)
        table = service.get_relationships()
        etl.io.totext(table, encoding='utf8', template='{relationship}\n')


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
        path = os.path.join(self.uri.path, 'RXNCONSO.RRF')
        rxnconso = etl \
            .fromcsv(path, delimiter='|') \
            .setheader(_RXNCONSO_FIELDS) \
            .select(lambda rec: rec['SAB'] == 'RXNORM') \
            .cut('RXCUI', 'CODE', 'STR')

        source = rxnconso.prefixheader('source.')
        target = rxnconso.prefixheader('target.')

        path = os.path.join(self.uri.path, 'RXNREL.RRF')
        rxnrel = etl \
            .fromcsv(path, delimiter='|') \
            .setheader(_RXNREL_FIELDS) \
            .select(lambda rec: rec['SAB'] == 'RXNORM') \
            .select(lambda rec: rec['STYPE1'] == 'CUI') \
            .select(lambda rec: rec['STYPE2'] == 'CUI') \
            .select(lambda rec: rec['REL'] == 'RB') \
            .cut('RXCUI1', 'RXCUI2')

        return rxnrel \
            .join(source, lkey='RXCUI1', rkey='source.RXCUI') \
            .join(target, lkey='RXCUI2', rkey='target.RXCUI') \
            .rowmap(_to_json, ['source.CODE', 'source.STR', 'target.CODE', 'target.STR']) \
            .setheader(['relationship'])
