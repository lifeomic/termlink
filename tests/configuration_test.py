import unittest

from termlink import configuration

class TestConfig(unittest.TestCase):

  def test_config_is_loaded(self):
    self.assertTrue('DEFAULT' in configuration.config)

  def test_get_user(self):
    self.assertIsNone(configuration.get_user())
  
  def test_get_account(self):
    self.assertIsNone(configuration.get_account())

  def test_get_project(self):
    self.assertIsNone(configuration.get_project())
