"""Verifies the 'models.py' module"""

from nose.tools import eq_

import json

from termlink.models import Coding, Relationship


def test_convert_coding_to_json():
    """Checks converting `Coding` to JSON"""

    system = 'system'
    version = 'version'
    code = 'code'
    display = 'display'

    coding = Coding(
        system=system,
        version=version,
        code=code,
        display=display
    )

    exp = {
        'type': 'coding',
        system: system,
        version: version,
        code: code,
        display: display
    }

    res = coding.to_json()

    eq_(json.dumps(exp), res)


def test_convert_empty_coding_to_json():
    """Checks converting `Coding` with no values to JSON"""

    coding = Coding()

    exp = {
        'type': 'coding',
        'system': None,
        'version': None,
        'code': None,
        'display': None
    }
    res = coding.to_json()

    eq_(json.dumps(exp), res)


def test_convert_partial_coding_to_json():
    """Checks converting `Coding` with some values to JSON"""

    system = 'system'

    coding = Coding(system=system)

    exp = {
        'type': 'coding',
        'system': system,
        'version': None,
        'code': None,
        'display': None
    }

    res = coding.to_json()

    eq_(json.dumps(exp), res)


def test_convert_relationship_to_json():
    """Checks converting `Relationship` to JSON"""

    equivalence = 'equivalence'
    system = 'system'
    version = 'version'
    code = 'code'
    display = 'display'
    
    source = Coding(
        system=system,
        version=version,
        code=code,
        display=display
    )

    target = Coding(
        system=system,
        version=version,
        code=code,
        display=display
    )

    relationship = Relationship(equivalence, source, target)

    exp = {
        'equivalence': equivalence,
        'source': {
            'type': 'coding',
            system: system,
            version: version,
            code: code,
            display: display
        },
        'target': {
            'type': 'coding',
            system: system,
            version: version,
            code: code,
            display: display
        }
    }

    res = relationship.to_json()

    eq_(json.dumps(exp), res)
