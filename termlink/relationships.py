import grequests

from dataclasses import dataclass
from urllib.parse import urlparse, urljoin

from termlink import configuration, sessions
from termlink.batches import batch as _batch
from termlink.configuration import logger

_URL = configuration.get_url()
_PATH = '/v1/terminology/projects/%s/relationships' % configuration.get_project()
_ENDPOINT = urljoin(_URL, _PATH)
_HEADERS = configuration.get_auth_headers()
_SESSION = sessions.get_session()

def _build_request(relationship):
  """
  Builds a PUT request from a :Relationship:.
  """
  return grequests.put(_ENDPOINT, headers=_HEADERS, json=relationship.to_json(), session=_SESSION)

def _parse_id(res):
  """
  Parses the 'id' from the responses 'location' header.
  """
  if res is None:
    logger.warn('Failed to create \'Relationship\'')
    return None
  
  if res.status_code is not 201:
    print(res)
    raise Exception('Failed to create \'Relationship\'')
  
  parts = res.headers['location'].split('/') 
  return parts[-1]

def create(relationships, batch_size=10, sleep=0):
  """
  Uploads a collection of :Relationship: values via the REST API.
  """
  _ids = []
  for batch in _batch(relationships, batch_size, sleep):
    requests = [ _build_request(relationship) for relationship in batch ]
    responses = grequests.map(requests, size=batch_size)
    _ids.extend([ _parse_id(res) for res in responses])
  
  return _ids

@dataclass
class Relationship:
  equivalence: str
  source: str
  target: str

  def to_json(self):
    return {
      'equivalence': self.equivalence,
      'source': self.source,
      'target': self.target
    }