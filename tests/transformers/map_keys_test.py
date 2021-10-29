import pytest

from resources import credito
from transformer.transformers.map_keys import MapKeys, MapKeysConfig


@pytest.fixture
def metadata_credito():
    return {"type": "deal", "origin": "pipedrive"}


@pytest.fixture(scope="session")
def target_data():
    return credito.target_data()


@pytest.fixture(scope="session")
def mapping():
    return credito.mapping()


@pytest.fixture
def nested_mapping():
    return {
        "id": "@{origin}_@{type}_id",
        "cliente.dados_bancarios.$[0].digito_agencia": "bank_data.$[0].agency_digit",
        "cliente.dados_bancarios.$[0].digito_conta": "bank_data.$[0].account_digit",
        "cliente.dados_bancarios.$[0].tipo_conta": "bank_data.$[0].account_type",
        "cliente.cpf": "client.cpf",
        "cliente.email": "client.email",
        "cliente.nome": "name",
        "operacoes_credito.$[0].condicao_credito.despesas.$[0].codigo": "bank_data.$[0].credit_operations.$[0].expenses_code",  # noqa
        "operacoes_credito.$[0].condicao_credito.valor_solicitado": "bank_data.$[0].credit_operations.$[0].valor_solicitado",  # noqa
    }


@pytest.fixture
def nested_target_data():
    return {
        "pipedrive_deal_id": 1645687,
        "client": {
            "cpf": "99915697902",
            "email": "marliaparecidaanadasneves-77@decode.buzz",
        },
        "name": "Marli Aparecida Ana das Neves",
        "bank_data": [
            {
                "agency_digit": "4",
                "account_digit": "1",
                "account_type": "CONTA_CORRENTE_INDIVIDUAL",
                "credit_operations": [
                    {"expenses_code": 1234, "valor_solicitado": 4117.48}
                ],
            }
        ],
    }


def test_mapped_dict(credito_payload, metadata_credito, target_data, mapping):
    mapper = MapKeys(config=MapKeysConfig(mapping=mapping, preserve_unmapped=False))
    assert mapper.transform(credito_payload, metadata_credito)[0] == target_data


def test_unflatted_dict(
    nested_mapping, nested_target_data, credito_payload, metadata_credito
):
    mapper = MapKeys(
        config=MapKeysConfig(mapping=nested_mapping, preserve_unmapped=False)
    )
    actual = mapper.transform(credito_payload, metadata_credito)[0]
    assert nested_target_data == actual
