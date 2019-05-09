"""Handles Gene Sets conversion.

This module provides methods to extract, transform and load relationships
defined by the Geneset dataset.

The download files for Geneset are provided at http://software.broadinstitute.org/gsea/msigdb/collections.jsp.
"""
import os
import csv
import json

from urllib.parse import urlparse

from termlink.commands import SubCommand
from termlink.models import Coding, Relationship, RelationshipSchema
from termlink.services import RelationshipService


def _to_json(rec, index):
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
        system="http://www.broadinstitute.org/gsea/msigdb",
        code=rec[index],
        display=rec[index]
    )

    target = Coding(
        system="http://www.broadinstitute.org/gsea/msigdb",
        code=rec[0],
        display=rec[0]
    )

    relationship = Relationship('subsumes', source, target)

    schema = RelationshipSchema()
    return json.dumps(schema.dump(relationship), sort_keys=True)


class Command(SubCommand):
    """
    A command executor for GSEA operations
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
        rows = service.get_relationships()
        for row in rows:
            print(row)


def validate_path(path):
    """
     Validates the file name for GSEA

    Args:
        path: The path/filename of the GSEA file
    """
    file_splits = os.path.basename(path).split('.')
    if file_splits[0] != 'msigdb':
        raise ValueError("only 'msigdb' is supported, %s not supported" % file_splits[0])

    if file_splits[3] != 'symbols':
        raise ValueError("only 'symbols' is supported, %s not supported" % file_splits[3])

    if file_splits[4] != 'gmt':
        raise ValueError("file type %s not supported" % file_splits[4])


class Service(RelationshipService):
    """Converts the GSEA database"""

    def __init__(self, uri):
        """
        Bootstraps a service

        Args:
            uri: URI to root location of .gmt files
        """

        if uri.scheme != 'file':
            raise ValueError("'uri.scheme' %s not supported" % uri.scheme)

        self.uri = uri

    def get_relationships(self):
        """
         Extracts the system entities from the GSEA file

        Returns:
            A new record containing a system, which is the JSON object
        """
        validate_path(self.uri.path)

        with open(self.uri.path) as gsea_tsv:
            gsea_reader = csv.reader(gsea_tsv, delimiter='\t')
            for gsea in gsea_reader:
                for i in range(2, len(gsea)):
                    yield _to_json(gsea, i)
