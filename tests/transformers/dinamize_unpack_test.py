import pytest
from devtools import debug

from resources import dinamize
from transformer.transformers.dinamize_unpack import DinamizeUnpack


@pytest.fixture(scope="session")
def dinamize_payload():
    return dinamize.payload()


@pytest.mark.xfail
def test_payload(dinamize_payload):
    debug(DinamizeUnpack(1).transform(dinamize_payload)[0])
    assert False, "Should implement this test!"
