"""Verifies the 'models.py' module"""

from urllib.parse import urljoin

from nose.tools import eq_

from requests_mock import Adapter

from termlink.client import Client
from termlink.models import Coding, Relationship


def test_coding_create():
    """Checks that a `Coding` can be created"""

    base = 'http://mock.com/'
    project = 'project'

    adapter = Adapter()
    adapter.register_uri('POST', base)

    url = urljoin(base, "/v1/terminology/projects/%s/codings" % project)
    client = Client(url=url, adapter=adapter)

    _id = '9761e60d-81d8-42e6-96a4-9b4cc8e2665f'
    headers = {
        'location': "/v1/terminology/projects/project/codings/%s" % _id
    }

    adapter.register_uri('PUT', url, headers=headers)

    system = 'system'
    version = 'version'
    code = 'code'
    display = 'display'

    coding = Coding(
        system=system,
        version=version,
        code=code,
        display=display
    )

    res = Coding.create(coding, project=project, client=client)

    eq_(_id, res)


def test_relationship_create():
    """Checks that `Relationship` can be created"""

    base = 'http://mock.com/'
    project = 'project'

    adapter = Adapter()
    adapter.register_uri('POST', base)

    url = urljoin(base, "/v1/terminology/projects/%s/relationships" % project)
    client = Client(url=url, adapter=adapter)

    _id = '9761e60d-81d8-42e6-96a4-9b4cc8e2665f'
    headers = {
        'location': "/v1/terminology/projects/project/relationships/%s" % _id
    }

    adapter.register_uri('PUT', url, headers=headers)

    equivalence = 'equivalence'
    source = 'source'
    target = 'target'

    relationship = Relationship(
        equivalence=equivalence,
        source=source,
        target=target
    )

    res = Relationship.create(relationship, project=project, client=client)

    eq_(_id, res)


def test_convert_coding_to_json():
    """Checks converting `Coding` to JSON"""

    system = 'system'
    version = 'version'
    code = 'code'
    display = 'display'

    coding = Coding(
        system=system,
        version=version,
        code=code,
        display=display
    )

    exp = {
        system: system,
        version: version,
        code: code,
        display: display
    }

    res = coding.to_json()

    eq_(exp, res)


def test_convert_empty_coding_to_json():
    """Checks converting `Coding` with no values to JSON"""

    coding = Coding()

    exp = {}
    res = coding.to_json()

    eq_(exp, res)


def test_convert_partial_coding_to_json():
    """Checks converting `Coding` with some values to JSON"""

    system = 'system'

    coding = Coding(system=system)

    exp = {system: system}
    res = coding.to_json()

    eq_(exp, res)


def test_convert_relationship_to_json():
    """Checks converting `Relationship` to JSON"""

    equivalence = 'equivalence'
    source = 'source'
    target = 'target'

    relationship = Relationship(equivalence, source, target)

    exp = {
        equivalence: equivalence,
        source: source,
        target: target
    }

    res = relationship.to_json()

    eq_(exp, res)
