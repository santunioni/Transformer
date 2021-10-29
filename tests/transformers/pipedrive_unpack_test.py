import pytest
from devtools import debug

from resources import pipedrive
from transformer.transformers.pipedrive_unpack import PipedriveUnpack


@pytest.fixture(scope="session")
def deal():
    return pipedrive.deal()


@pytest.fixture(scope="session")
def person():
    return pipedrive.person()


@pytest.fixture(scope="session")
def organization():
    return pipedrive.organization()


@pytest.mark.xfail
def test_deal(deal):
    debug(PipedriveUnpack(1).transform(deal)[0])
    assert False, "Should implement this test!"


@pytest.mark.xfail
def test_person(person):
    debug(PipedriveUnpack(1).transform(person)[0])
    assert False, "Should implement this test!"


@pytest.mark.xfail
def test_organization(organization):
    debug(PipedriveUnpack(1).transform(organization)[0])
    assert False, "Should implement this test!"
