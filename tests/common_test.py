"""Verifies the 'common.py' module"""

from nose.tools import eq_, ok_, raises

import os

from argparse import Namespace
from pronto import Term
from tempfile import mkstemp

from termlink.common import _to_coding, _to_relationship, execute
from termlink.models import Coding, Relationship

@raises(ValueError)
def test_uri_scheme():
    """An unsupported URI scheme throws a ValueError"""
    ok_(execute(Namespace(uri='foo://bar')))

def test_obo():
    """Tests the conversion of a .obo file"""
    fd, path = mkstemp(suffix='.obo')
    
    with open(path, 'w') as f:
        f.write(
            """
            format-version: 1.2
            ontology: https://lifeomic.github.io/termlink//ontologies/2019/5/termlink

            [Term]
            id: 55f41bdb_1005_496c_aeae_ab127e78c525
            name: Root

            [Term]
            id: 61e2ec3e_6102_44dc_9f3c_3445e45dbf9e
            name: Leaf
            is_a: 55f41bdb_1005_496c_aeae_ab127e78c525 ! Root
            """
        )

    uri = f"file://{path}"
    system = 'https://lifeomic.github.io/termlink/'
    execute(Namespace(uri=uri, system=system))

    os.close(fd)

def test_to_coding():
    """Checks that a term is properly converted"""

    system = "http://snomed.info/sct"
    term = Term(id='SNOMEDCT_US:25064002', name='Headache')

    res = _to_coding(term, system)

    exp = Coding(
        system=system,
        code='25064002',
        display='Headache'
    )

    eq_(exp, res)

def test_to_coding_without_colon():
    """Checks that a term without a ':' is properly converted"""

    system = "http://snomed.info/sct"
    term = Term(id='25064002', name='Headache')

    res = _to_coding(term, system)

    exp = Coding(
        system=system,
        code='25064002',
        display='Headache'
    )

    eq_(exp, res)

def test_to_json():
    """Checks that a source, equivalence and target and properly converted"""

    system = "http://snomed.info/sct"
    source = Term(id='SNOMEDCT_US:735938006', name='Acute headache')
    equivalence = 'subsumes'
    target = Term(id='SNOMEDCT_US:25064002', name='Headache')

    res = _to_relationship(source, equivalence, target, system)

    exp = Relationship(
        equivalence='subsumes',
        source=Coding(
            system=system,
            code='735938006',
            display='Acute headache'
        ),
        target=Coding(
            system=system,
            code='25064002',
            display='Headache'
        )
    )

    eq_(exp, res)
