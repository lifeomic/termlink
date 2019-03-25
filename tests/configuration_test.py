"""Verifies the 'configuration.py' module."""
import unittest

from termlink import configuration


class TestConfig(unittest.TestCase):
    """
    Verifies that various properties are configured correctly.
    """
    def test_config_is_loaded(self):
        """Checks that the 'DEFAULT' environment is available"""
        self.assertTrue("DEFAULT" in configuration.config)

    def test_get_user(self):
        """Checks that the 'user' is available"""
        self.assertIsNone(configuration.get_user())

    def test_get_account(self):
        """Checks that the 'account' is available"""
        self.assertIsNone(configuration.get_account())

    def test_get_project(self):
        """Checks that the 'project' is available"""
        self.assertIsNone(configuration.get_project())
