"""Provides client libraries for communicating with the LifeOmic API"""

from urllib.parse import urljoin, urlparse

from ratelimit import limits

from termlink.adapter import DEFAULT as DEFAULT_ADAPTER
from termlink.configuration import Config
from termlink.session import Session

FIVE_MINUTES = 300

_configuration = Config()

class Client:
    """An HTTP client to communicate with the API"""

    def __init__(
            self,
            account=_configuration.get_property('LO_ACCOUNT'),
            api_key=_configuration.get_property('LO_API_KEY'),
            url=_configuration.get_property('API_URL'),
            adapter=DEFAULT_ADAPTER):
        """
        Creates a new API client.

        Args:
            account (str):          a valid LifeOmic account
            api_key (str):          a valid LifeOmic API key
            url (str):              the API URL
            adapter (HTTPAdapter):  an HTTPAdapter
        """

        if url is None:
            raise TypeError("'url' is required")

        session = Session()
        if account and api_key:
            session.setup_authorization(account, api_key)

        parsed = urlparse(url)
        prefix = parsed[0] + "://"
        session.mount(prefix, adapter)

        self.session = session
        self.url = url

    @limits(calls=20_000, period=FIVE_MINUTES)
    def request(self, method, path, data):
        """
        A facade around :func:`requests.request` that provides rate limiting.

        Args:
            method: request method
            path:   URL path
            data:   JSON  data

        Returns:
            A :class:`Response <Response>` object
        """
        url = urljoin(self.url, path)
        return self.session.request(method, url, json=data)
