import unittest

import asyncio

from termlink.codings import HOSTNAME, PORT, PROTOCOL, URL, Coding, upload

class TestConfig(unittest.TestCase):

  def test_hostname_is_set(self):
    self.assertIsNotNone(HOSTNAME)

  def test_port_is_set(self):
    self.assertIsNotNone(PORT)

  def test_protocol_is_set(self):
    self.assertIsNotNone(PROTOCOL)

  def test_url_is_set(self):
    self.assertIsNotNone(URL)
      
