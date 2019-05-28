"""Verifies the 'gsea.py' module"""
import json

from argparse import Namespace

from nose.tools import eq_, raises

from termlink.gsea import execute


@raises(ValueError)
def test_uri_scheme():
    """A URI scheme of 'file://' is required"""
    execute(Namespace(uri='foo://bar'))


@raises(ValueError)
def test_uri_filename_database():
    "A invalid file name throws a ValueError"
    execute(Namespace(uri='file:///invalid.foo.bar.symbols.gmt'))


@raises(ValueError)
def test_uri_filename_type():
    "A invalid file name throws a ValueError"
    execute(Namespace(uri='file:///msigdb.foo.bar.invalid.gmt'))


@raises(ValueError)
def test_uri_filename_suffix():
    "A invalid file name throws a ValueError"
    execute(Namespace(uri='file:///msigdb.foo.bar.symbols.invalid'))
