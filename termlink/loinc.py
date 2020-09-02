"""Handles LOINC conversion.

This module provides methods to extract, transform and load relationships
defined by the LOINC dataset.

The download files for LOINC are provided at https://loinc.org/downloads/.
"""
import os
import json
import re

from urllib.parse import urlparse

import petl as etl

from termlink.commands import SubCommand
from termlink.models import Coding, Relationship, RelationshipSchema

_SYSTEM = 'http://loinc.org'


def _parse_version(path: str):
    try:
        pattern = re.compile('Loinc_([\d.]*)_MultiAxialHierarchy')
        match = pattern.search(path)
        return match.group(1)
    except:
        raise RuntimeError('Unable to parse version from path', path)

def _to_json(rec: etl.Record):
    """Converts a record to a formatted `Relationship` in JSON form.

    Args:
        rec: A table record

    Returns:
        A new record containing a single field, which is the JSON object
    """
    coding = Coding(
        system=_SYSTEM, 
        code=rec['source.CODE'],
        display=rec['source.CODE_TEXT'],
        version=rec.get('version')
    )

    parent = Coding(
        system=_SYSTEM, 
        code=rec['source.IMMEDIATE_PARENT'], 
        display=rec['target.CODE_TEXT'],
        version=rec.get('version')
    )

    relationships = [
        Relationship('subsumes', coding, parent),
        Relationship('specializes', parent, coding)
    ]

    schema = RelationshipSchema()
    return map(lambda relationship: [json.dumps(schema.dump(relationship))], relationships)


class Command(SubCommand):
    "A command executor for LOINC operations"

    @staticmethod
    def execute(args):
        """Prints a JSON array of `Relationship` objects to stdout

        Args:
            args: `argparse` parsed arguments
        """
        uri = urlparse(args.uri)
        service = Service(uri, args.versioned)
        table = service.get_relationships()
        etl.totext(table, source=None, encoding='utf8', template='{relationship}\n')


class Service:
    """Converts the LOINC Table Core files"""

    def __init__(self, uri, versioned):
        """Bootstraps a service

        Args:
            uri: URI to root location of the LOINC Table Core download files
        """

        if uri.scheme != 'file':
            raise ValueError("'uri.scheme' %s not supported" % uri.scheme)

        self.uri = uri
        self.versioned = versioned

    def get_relationships(self):
        "Parses a list of `Relationship` objects."
        path = os.path.join(self.uri.path, 'MultiAxialHierarchy.csv')
        hierarchy = etl.fromcsv(path, delimiter=',')
        hierarchy = etl.cut(hierarchy, ['IMMEDIATE_PARENT', 'CODE', 'CODE_TEXT'])
        parents = etl.cut(hierarchy, ['CODE', 'CODE_TEXT'])
        hierarchy = etl.selectne(hierarchy, 'IMMEDIATE_PARENT', '')
        hierarchy = etl.leftjoin(hierarchy, parents, lkey='IMMEDIATE_PARENT', rkey='CODE', lprefix='source.', rprefix='target.')
        hierarchy = etl.distinct(hierarchy)
        if self.versioned:
            version = _parse_version(path)
            hierarchy = etl.addfield(hierarchy, 'version', version)
        hierarchy = etl.rowmapmany(hierarchy, _to_json, ['relationship'])
        return hierarchy
