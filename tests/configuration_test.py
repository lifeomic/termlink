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


    """Checks the default API URL is set"""
def test_lifeomic_account():
    """Checks the default LifeOmic account is set"""
    ok_(configuration.get_property('LO_ACCOUNT'))


def test_lifeomic_user():
    """Checks the default LifeOmic user is set"""
    ok_(configuration.get_property('LO_USER'))


def test_lifeomic_project():
    """Checks the default LifeOmic project is set"""
    ok_(configuration.get_property('LO_PROJECT'))


def test_lifeomic_api_key():
    """Checks the default LifeOmic API key is set"""
    ok_(configuration.get_property('LO_API_KEY'))


def test_the_configuration_is_valid():
    """Checks that the configuration is valid"""
    ok_(configuration.is_valid())
