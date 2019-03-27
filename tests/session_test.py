"""Validates the 'session.py' module"""

from nose.tools import ok_, eq_

from termlink.session import Session


def test_setup_authorization():
    """Checks that the authorization headers are configured properly"""

    account = 'account'
    api_key = 'api_key'

    session = Session()

    session.setup_authorization(account, api_key)

    headers = session.headers

    ok_(headers)

    authorization = headers['Authorization']
    eq_("Bearer %s" % api_key, authorization)

    _account = headers['LifeOmic-Account']
    eq_(account, _account)
