"""Verifies the 'common.py' module"""

from nose.tools import eq_

from pronto import Term

from termlink.common import _to_coding, _to_relationship
from termlink.models import Coding, Relationship


def test_to_coding():
    """Checks that a term is properly converted to a coding"""

    system = "http://snomed.info/sct"
    term = Term(id='SNOMEDCT_US:25064002', name='Headache')

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
