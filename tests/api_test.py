"""Verifies the 'api.py' module"""

from nose.tools import eq_, ok_

from termlink.api import build_authentication_headers
from termlink.configuration import Config

configuration = Config()

def test_build_authentication_headers():
    """Checks that the authenication headers have been configured properly"""

    account = configuration.get_property('LO_ACCOUNT')
    api_key = configuration.get_property('LO_API_KEY')

    headers = build_authentication_headers()

    ok_(headers)

    authorization = headers['Authorization']
    eq_("Bearer %s" % api_key, authorization)

    _account = headers['LifeOmic-Account']
    eq_(account, _account)
    