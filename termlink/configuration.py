"""
Utility method for loading properties form the configuration file and environment variables.
"""

import configparser
import logging
import os
import validators

# Relative location of configuration file
_PROGRAM_CONFIG = '../config.ini'

_environment = os.getenv("ENV", 'DEFAULT').upper()

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

            # Create an application logger
            logger = logging.getLogger("termlink")
            logging.basicConfig()

            # Set the logging level
            if _environment == "TEST":
                logger.setLevel(logging.DEBUG)
            else:
                logger.setLevel(logging.INFO)

            logger.info("The logging level has been set to %s", logger.level)

            parser = configparser.ConfigParser(os.environ, strict=False)
            
            # Get the absolute path based on the execution directory
            root = os.path.abspath(os.path.dirname(__file__))
            config = os.path.join(root, _PROGRAM_CONFIG)
            
            configs = [config]
            parser.read(configs)

            self.logger = logger
            self.parser = parser

    instance = None

    def __init__(self):
        if not Config.instance:
            Config.instance = Config.__Config()

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def get_property(self, property_name, default=None):
        """Get a property value from the configuration.

        The os environment variables are first checked. If the property
        does not exists there it is read from the configuration file.

        Args:
            property_name (str):    A name, or key, of a property

        Returns:
            The property value associated with the property_name
        """
        if property_name in os.environ:
            return os.environ[property_name]

        return self.parser.get(_environment, property_name, fallback=default)

    def is_valid(self):
        """Asserts that the configuration is correct.

        This method checks various required properties for existence and
        checks some properties for proper formatting.
        """

        # Validate that the API URL is properly formatted
        return validators.url(self.get_property('API_URL'))
