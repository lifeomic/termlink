"""
Utility method for loading properties form the configuration file and environment variables.
"""

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


class Config:
    """A configuration singleton"""

    class __Config:
        """A configuration supplier.

        An object for reading configuration properties. Properties are injected with
        the following priority. Properties with higher priority overwrite those
        with lower priority.

        1. Program defaults
        2. The 'DEFAULT' section in 'config.ini'
        3. The environment in the 'config.ini' file set by the 'ENV' environment variable
        4. Runtime system environment variables
        """

        def __init__(self):

            environment = os.getenv("ENV", _DEFAULT_ENV).upper()

            # Create an application logger
            logger = logging.getLogger("termlink")
            logging.basicConfig()

            # Set the logging level
            if environment == "TEST":
                logger.setLevel(logging.DEBUG)
            if environment == "DEV":
                logger.setLevel(logging.DEBUG)
            else:
                logger.setLevel(logging.INFO)

            logger.info("The logging level has been set to %s", logger.level)

            parser = configparser.RawConfigParser()

            # Load program defaults
            parser.read_dict({'__PROGRAM': _DEFAULT_CONF})

            # Load user level `config.ini` file
            config_file = os.getenv("CONFIG", "config.ini")
            parser.read(config_file)

            # Load system level environment variables
            parser.read_dict({'__SYSTEM': os.environ.copy()})

            # Copy configuration into a :dict: respecting priority
            config = {}
            sections = ['__PROGRAM', _DEFAULT_ENV, environment, '__SYSTEM']
            for section in sections:
                if parser.has_section(section):
                    for k, v in parser.items(section):
                        config[k] = v

            self.logger = logger
            self.parser = parser
            self.config = config

    instance = None

    def __init__(self):
        if not Config.instance:
            Config.instance = Config.__Config()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def get_property(self, property_name):
        """Get a property value from the configuration.

        Args:
            property_name (str):    A name, or key, of a property

        Returns:
            The property value associated with the property_name
        """

        key = property_name.lower()

        # Avoid KeyError
        if key not in self.config.keys():
            return None

        return self.config[key]

    def is_valid(self):
        """Asserts that the configuration is correct.

        This method checks various required properties for existence and
        checks some properties for proper formatting.
        """

        # Validate that the API URL is properly formatted
        return validators.url(self.get_property('API_URL'))
