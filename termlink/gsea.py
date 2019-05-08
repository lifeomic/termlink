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
from termlink.services import RelationshipService


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
            print(json.dumps(row))


def build_node(gsea, i):
    """
     Extracts single target/source system from a tab delimited/iterator
    """
    return {'type': 'coding', 'display': gsea[i], 'system': 'http://www.broadinstitute.org/gsea/msigdb',
            'version': 'null', 'code': gsea[i]}


def generate_row(gsea, i):
    """
     Extracts single system from a tab delimited/iterator
    """
    return {'target': build_node(gsea, 0), 'equivalence': 'subsumes', 'source': build_node(gsea, i)}


def validate_path(path):
    """
     Validates the file name for GSEA
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
        """
        validate_path(self.uri.path)

        rows = []
        with open(self.uri.path) as gsea_tsv:
            gsea_reader = csv.reader(gsea_tsv, delimiter='\t')
            for gsea in gsea_reader:
                for i in range(2, len(gsea)):
                    row = generate_row(gsea, i)
                    rows.append(row)
        return rows
