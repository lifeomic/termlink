"""Verifies the 'rxnorm.py' module"""

from urllib.parse import urlparse

from nose.tools import ok_, raises, eq_

from petl import Record

from termlink.rxnorm import Service, _to_json


def test_service_uri_can_be_file():
    """Checks that a uri.scheme of 'file' is ok"""
    uri = urlparse("file://")
    ok_(Service(uri=uri))


@raises(ValueError)
def test_service_uri_requires_scheme_file():
    """Checks that a uri.scheme of 'foobar' throws a ValueError"""
    uri = urlparse("foobar://")
    Service(uri=uri)


def test_to_json():
    """Checks that a record is properly converted to .json"""

    fields = ['source.CODE', 'source.STR', 'target.CODE', 'target.STR']
    values = (
        '313782',
        'Acetaminophen 325 MG Oral Tablet',
        '1152843',
        'Acetaminophen Pill'
    )

    src = Record(values, fields)
    res = _to_json(src)
    ok_(res[0])
