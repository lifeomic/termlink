"""Utility methods for interacting with the API"""

from termlink.configuration import Config

configuration = Config()

def build_authentication_headers():
    """Builds the required authentication headers.

    This method creates a :dict: containing the required headers for
    authentication against the API.
    """

    account = configuration.get_property('LO_ACCOUNT')
    if account is None:
        raise ValueError("The configuration property 'LO_ACCOUNT' is required")

    api_key = configuration.get_property('LO_API_KEY')
    if api_key is None:
        raise ValueError("The configuration property 'LO_API_KEY' is required")

    return {
        "Authorization": "Bearer %s" % api_key,
        "LifeOmic-Account": account
    }
