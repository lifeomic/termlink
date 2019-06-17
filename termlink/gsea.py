"""Handles Gene Sets conversion.

This module provides methods to extract, transform and load relationships
defined by the Geneset dataset.

The download files for Geneset are provided at http://software.broadinstitute.org/gsea/msigdb/collections.jsp.
"""

import csv
import json
import os

from re import match
from urllib.parse import urlparse

from termlink.models import Coding, Relationship, RelationshipSchema

_filename_regex = r'msigdb\..*\.symbols\.gmt'


def _to_relationship(rec, index):
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

    return Relationship('subsumes', source, target)


def _get_relationships(input_file):
    '''Extracts the system entities from the GSEA file

    Args:
        uri: a URI for the GSEA file on the local filesystem

    Returns:
        yields relationships
    '''
    with open(input_file) as f:
        reader = csv.reader(f, delimiter='\t')
        for row in reader:
            for i in range(2, len(row)):
                yield _to_relationship(row, i)


def execute(args):
    '''Converts the GSEA ontology.

    Args:
        args:   command line arguments from argparse
    '''

    uri = urlparse(args.uri)
    if uri.scheme != 'file':
        raise ValueError(f"uri.scheme '{uri.scheme}' is not supported")

    input_file = uri.path
    if not match(_filename_regex, os.path.basename(input_file)):
        raise ValueError(
            f"File type is incorrect. Expected to match regular expression: '{_filename_regex}'. Found '{input_file}'.")

    schema = RelationshipSchema()

    if args.output:
        open('file.txt', 'w').close()

    for relationship in _get_relationships(input_file):
        o = json.dumps(schema.dump(relationship))
        if args.output:
            with open(args.output, 'a') as out_file:
                out_file.write(o + '\n')
        else:
            print(o)

