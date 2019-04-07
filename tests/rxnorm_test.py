"""Verifies the 'rxnorm.py' module"""

from urllib.parse import urlparse

from nose.tools import ok_, raises

from termlink.rxnorm import Service


def test_service_uri_can_be_file():
    """Checks that a uri.scheme of 'file' is ok"""
    uri = urlparse("file://")
    ok_(Service(uri=uri))


@raises(ValueError)
def test_service_uri_requires_scheme_file():
    """Checks that a uri.scheme of 'foobar' throws a ValueError"""
    uri = urlparse("foobar://")
    Service(uri=uri)
