from typing import Dict

import pytest

from resources import credito, pipedrive


@pytest.fixture
def data() -> Dict:
    return {
        "id": 1645687,
        "true": True,
        "a": "A-VALUE",
        "b": "B-VALUE",
        "e": {"a": "s", "g": [1, 2]},
        "f": [1, 2, 3, 4],
        "email_1": "lala@decode.buzz",
        "email_2": "lele@decode.buzz",
        "email_3": "lili@decode.buzz",
    }


@pytest.fixture(
    scope="session",
    params=[
        credito.payload(),
        pipedrive.deal(),
        pipedrive.organization(),
        pipedrive.person(),
    ],
)
def highly_nested_data(request):
    return request.param


@pytest.fixture(scope="session")
def credito_payload():
    return credito.payload()
