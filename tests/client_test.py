"""Validates the 'client.py" module"""

from nose.tools import ok_

from termlink.client import Client

def test_client_construction():
    """Checks that the client can be instantiated"""

    account = 'account'
    api_key = 'api_key'
    url = 'url'

    client = Client(account, api_key, url)

    ok_(client)
