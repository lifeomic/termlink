"""Handles conversions of common ontology formats

This module provides support for converting common ontology formats. The 
following file types are supported:

- .obo: https://owlcollab.github.io/oboformat/doc/GO.format.obo-1_4.html
- .owl: https://www.w3.org/OWL/

"""

import json

from urllib.parse import urlparse

from pronto import Ontology

from termlink.commands import SubCommand
from termlink.models import Coding, Relationship, RelationshipSchema


def _to_coding(term, system):
    """Converts a term into a `Coding`.

    Args:
        term: A `pronto.Term`

    Returns:
        a `termlink.models.Coding`
    """
    if ':' in term.id:
        code = term.id.split(':')[1]
    else:
        code = term.id

    return Coding(
        system=system,
        code=code,
        display=term.name
    )


def _to_relationship(source, equivalence, target, system):
    """Converts a source and target `pronto.Term` into a JSON object.

    Args:
        source: a `pronto.Term`
        equivalence: a concept map equivalence
        target: a `pronto.Term`

    Returns:
        a 'termlink.models.Relationship` in JSON form
    """
    source = _to_coding(source, system)
    target = _to_coding(target, system)
    return Relationship(equivalence, source, target)


class Command(SubCommand):
    "A command executor for generic ontology files."
    @staticmethod
    def execute(args):
        uri = urlparse(args.uri)
        system = args.system
        service = Service(uri, system)
        relationships = service.get_relationships()
        schema = RelationshipSchema()
        relationships = [schema.dump(relationship)
                         for relationship in relationships]
        print(json.dumps(relationships))


class Service:
    "Converts the Human Phenotype Ontology"

    def __init__(self, uri, system):
        """Bootstraps a service

        Args:
            uri: URI to the file location
            system: The code system identifer
        """
        if uri.scheme != 'file':
            raise ValueError("'uri.scheme' %s not supported" % uri.scheme)

        self.uri = uri
        self.system = system

    def get_relationships(self):
        """Parses a list of `Relationship` objects

        Returns:
            yields `Relationship`s in JSON form
        """
        ontology = Ontology(self.uri.path)

        # child to parent relationships
        for term in ontology:
            for child in term.children:
                yield _to_relationship(child, "subsumes", term, self.system)

        # parent to child relationships
        for term in ontology:
            for parent in term.parents:
                yield _to_relationship(parent, "specializes", term, self.system)
