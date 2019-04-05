"""Verifies the 'configuration.py' module."""
from nose.tools import ok_

from termlink.configuration import Config

configuration = Config()


def test_configuration_is_loaded():
    """Checks that the configuration is loaded"""
    ok_(configuration)


def test_logger_is_configured():
    """Checks that the application logger has been configured"""
    ok_(configuration.logger)


def test_the_configuration_is_valid():
    """Checks that the configuration is valid"""
    ok_(configuration.is_valid())
