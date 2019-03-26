"""
Utility method for loading properties form the configuration file and environment variables.
"""
from dataclasses import dataclass
from typing import Any

import configparser
import logging
import os
import validators

_DEFAULT_ENV = "DEFAULT"

# A simple default configuration that is used for testing and bootstrapping
_DEFAULT_CONF = {

    'API_URL': 'http://localhost:8080',

    'LO_ACCOUNT': 'Test Account',
    'LO_USER': 'Test User',
    'LO_PROJECT': 'Test Project',
    'LO_API_KEY': 'Test API Key'
}

@dataclass
class Config():
    """A configuration object.

    An object for reading configuration properties. Properties are injected with
    the following priority. Properties with higher priority overwrite those
    with lower priority.

    1. Environment in the 'config.ini' file set by the 'ENV' environment variable.
    2. The 'DEFAULT' enviornment in 'config.ini'
    3. Default configuration from the 'conf' dict above.
    """

    logger: Any

    def __init__(self):

        environment = os.getenv("ENV", _DEFAULT_ENV)

        # Create an application logger
        logger = logging.getLogger("termlink")
        logging.basicConfig()
        if environment == "test":
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)

        logger.info("The logging level has been set to %s", logger.level)
        self.logger = logger

        # Import the application configuration
        config_file = os.getenv("CONFIG", "config.ini")

        parser = configparser.ConfigParser()
        parser.read(config_file)

        if environment not in parser:
            environment = _DEFAULT_ENV

        self._config = {
            **_DEFAULT_CONF,
            **parser[_DEFAULT_ENV],
            **parser[environment],
            **os.environ
        }

    def get_property(self, property_name):
        """Get a property value from the configuration.

        Args:
            property_name (str):    A name, or key, of a property

        Returns:
            The property value associated with the property_name
        """

        if property_name not in self._config.keys(): # avoid KeyError
            return None

        return self._config[property_name]

    def is_valid(self):
        """Asserts that the configuration is correct.

        This method checks various required properties for existence and
        checks some properties for proper formatting.
        """

        # Validate that the API URL is properly formatted
        return validators.url(self.get_property('API_URL'))


def get_auth_headers():
    """Gets HTTP headers with authentication"""

    account = None
    if account is None:
        raise Exception("'account' is required")

    access_key = None
    if access_key is None:
        raise Exception("'access_key' is required")

    return {
        "Authorization": "Bearer %s" % access_key,
        "LifeOmic-Account": account
    }
