"""
Utility method for loading properties form the configuration file and environment variables.
"""

import configparser
import logging
import os

from urllib.parse import urlparse, urljoin

_CONFIG = 'config.ini'
_ENV = 'DEFAULT'

LOCATION = os.getenv('CONFIG', _CONFIG)

config = configparser.ConfigParser()
config.read(LOCATION)

env = os.getenv('ENV', _ENV)

logger = logging.getLogger('termlink')
logging.basicConfig()
if env == 'test':
  logger.setLevel(logging.DEBUG)
else:
  logger.setLevel(logging.INFO)

# If the environment is not in the configuration file revert to default configuration.
environment = env
if environment not in config:
  logger.warning('Environment \'%s\' not in configuration file.' % environment)
  environment = _ENV

def get_property(prop):
  """Reads property from configuration file.

  The environment of the configuration file that is read from is based on the environment variable 'ENV'.

  Parameters
  ----------
  prop : str
      Name of property

  Returns
  -------
  str
      Value of property in configuration file
  """
  logger.debug('Reading property \'%s\' from \'%s\' environment configuration' % (prop, environment))
  return config[environment][prop]

def get_user():
  """Gets the LO_USER environment variable"""
  return os.environ.get('LO_USER')

def get_account():
  """Gets the LO_ACCOUNT environment variable"""
  return os.environ.get('LO_ACCOUNT')

def get_project():
  """Gets the LO_PROJECT environment variable"""
  return os.environ.get('LO_PROJECT')

def get_access_key():
  """Gets the LO_ACCESS_KEY environment variable"""
  return os.environ.get('LO_ACCESS_KEY')

def get_url():
  """Gets the API url based on the configuration properties"""
  
  protocol = get_property('PROTOCOL')
  if protocol is None:
    raise Exception("'PROTOCOL' is required")
  
  hostname = get_property('HOSTNAME')
  if hostname is None:
    raise Exception("'HOSTNAME' is required")
    
  port = get_property('PORT')
  if port is None:
    raise Exception("'PORT' is required")

  url = urlparse('%s://%s:%s' % (protocol, hostname, port)).geturl()
  return url

def get_auth_headers():
  """Gets HTTP headers with authentication"""
  
  account = get_account()
  if account is None:
    raise Exception("'account' is required")

  access_key = get_access_key()
  if access_key is None:
    raise Exception("'access_key' is required")

  return {
    'Authorization': "Bearer %s" % access_key,
    'LifeOmic-Account': account,
  }