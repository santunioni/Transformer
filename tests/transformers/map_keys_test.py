import pytest
from devtools import debug

from transformer.transformers.map_keys import MapKeys, MapKeysConfig


@pytest.fixture
def metadata_credito():
    return {"type": "deal", "origin": "pipedrive"}


@pytest.fixture
def target_data():
    return {
        "address": "ARSE 32 Alameda 1",
        "address_number": "326",
        "address_type": "FISICO",
        "annual_appropriation_rate": 23.8721,
        "annual_cet_rate": 25.6687,
        "annual_reference_rate": 24.238,
        "bank_account_digit": "1",
        "bank_account_number": "71444",
        "bank_account_type": "CONTA_CORRENTE_INDIVIDUAL",
        "bank_ag_digit": "4",
        "bank_ag_number": "265",
        "bank_number": "001",
        "benefit_type_code": 42,
        "birth_date": "18-02-1989",
        "city": "Palmas",
        "client_value": 4117.48,
        "consigned_margin": 100,
        "cpf": "99915697902",
        "deadline": 84,
        "document_emission_date": "10-02-2000",
        "document_number": "407941319",
        "email": "marliaparecidaanadasneves-77@decode.buzz",
        "expenses_code": 1234,
        "expenses_financed": "sim",
        "expenses_maximum_value": 2,
        "expenses_minimum_value": 1,
        "financed_value": 4246.6,
        "financing_table_code": "703347",
        "financing_table_description": "INSS_NOV_DIG_NORMAL",
        "first_due_date": "07-10-2021",
        "installment_value": 100,
        "iof_value": 129.12,
        "last_due_date": "07-09-2028",
        "lp_form_code": 7,
        "marital_status": "CASADO",
        "method": "VALOR_SOLICITADO",
        "monthly_appropriation_rate": 1.8,
        "monthly_cet_rate": 1.8957,
        "monthly_income": 1000,
        "monthly_reference_rate": 1.825,
        "name": "Marli Aparecida Ana das Neves",
        "nationality": "BRASILEIRA",
        "neighborhood": "Plano Diretor Sul",
        "net_value": 4117.48,
        "optin": True,
        "org_code": "000501",
        "phone": "(63) 36366-1878",
        "pipedrive_deal_id": 1645687,
        "ppe": False,
        "preferencial_enrollment": "0000000000",
        "product_code": "000440",
        "product_description": "INSS - MARGEM",
        "raw_value": 8400,
        "requested_value": 4117.48,
        "state": "TO",
        "zip_code": "77021-050",
    }


@pytest.fixture
def mapping():
    return {
        "id": "@{origin}_@{type}_id",
        "cliente.codigo_orgao": "org_code",
        "cliente.codigo_tipo_beneficio": "benefit_type_code",
        "cliente.cpf": "cpf",
        "cliente.dados_bancarios.$[0].digito_agencia": "bank_ag_digit",
        "cliente.dados_bancarios.$[0].digito_conta": "bank_account_digit",
        "cliente.dados_bancarios.$[0].numero_agencia": "bank_ag_number",
        "cliente.dados_bancarios.$[0].numero_banco": "bank_number",
        "cliente.dados_bancarios.$[0].numero_conta": "bank_account_number",
        "cliente.dados_bancarios.$[0].tipo_conta": "bank_account_type",
        "cliente.data_emissao_documento": "document_emission_date",
        "cliente.data_nascimento": "birth_date",
        "cliente.email": "email",
        "cliente.enderecos.$[0].bairro": "neighborhood",
        "cliente.enderecos.$[0].cep": "zip_code",
        "cliente.enderecos.$[0].cidade": "city",
        "cliente.enderecos.$[0].estado": "state",
        "cliente.enderecos.$[0].logradouro": "address",
        "cliente.enderecos.$[0].numero": "address_number",
        "cliente.enderecos.$[0].tipo": "address_type",
        "cliente.estado_civil": "marital_status",
        "cliente.matricula_preferencial": "preferencial_enrollment",
        "cliente.nacionalidade": "nationality",
        "cliente.nome": "name",
        "cliente.numero_documento": "document_number",
        "cliente.opt_in": "optin",
        "cliente.pessoa_politicamente_exposta": "ppe",
        "cliente.renda_mensal": "monthly_income",
        "cliente.telefone": "phone",
        "cliente.valor": "consigned_margin",
        "creditoconsignado_lp_ultimo_passo_form": "lp_form_code",
        "motivo_erro": "reason_error",
        "operacoes_credito.$[0].condicao_credito.codigo_produto": "product_code",
        "operacoes_credito.$[0].condicao_credito.codigo_tabela_financiamento": "financing_table_code",
        "operacoes_credito.$[0].condicao_credito.descricao_produto": "product_description",
        "operacoes_credito.$[0].condicao_credito.descricao_tabela_financiamento": "financing_table_description",
        "operacoes_credito.$[0].condicao_credito.despesas.$[0].codigo": "expenses_code",
        "operacoes_credito.$[0].condicao_credito.despesas.$[0].financiada": "expenses_financed",
        "operacoes_credito.$[0].condicao_credito.despesas.$[0].grupo": "expenses_group",
        "operacoes_credito.$[0].condicao_credito.despesas.$[0].inclusa": "expenses_included",
        "operacoes_credito.$[0].condicao_credito.despesas.$[0].numero_item": "expenses_item_number",
        "operacoes_credito.$[0].condicao_credito.despesas.$[0].obrigatoria": "expenses_mandatory",
        "operacoes_credito.$[0].condicao_credito.despesas.$[0].tipo": "expenses_type",
        "operacoes_credito.$[0].condicao_credito.despesas.$[0].valor_calculado": "expenses_caculated_value",
        "operacoes_credito.$[0].condicao_credito.despesas.$[0].valor_maximo": "expenses_maximum_value",
        "operacoes_credito.$[0].condicao_credito.despesas.$[0].valor_minimo": "expenses_minimum_value",
        "operacoes_credito.$[0].condicao_credito.despesas.$[0].valor_padrao_mutavel": "expenses_changeable_default_value",  # noqa
        "operacoes_credito.$[0].condicao_credito.metodo": "method",
        "operacoes_credito.$[0].condicao_credito.prazo": "deadline",
        "operacoes_credito.$[0].condicao_credito.primeiro_vencimento": "first_due_date",
        "operacoes_credito.$[0].condicao_credito.taxa_apropriacao_anual": "annual_appropriation_rate",
        "operacoes_credito.$[0].condicao_credito.taxa_apropriacao_mensal": "monthly_appropriation_rate",
        "operacoes_credito.$[0].condicao_credito.taxa_cet_anual": "annual_cet_rate",
        "operacoes_credito.$[0].condicao_credito.taxa_cet_mensal": "monthly_cet_rate",
        "operacoes_credito.$[0].condicao_credito.taxa_referencia_anual": "annual_reference_rate",
        "operacoes_credito.$[0].condicao_credito.taxa_referencia_mensal": "monthly_reference_rate",
        "operacoes_credito.$[0].condicao_credito.ultimo_vencimento": "last_due_date",
        "operacoes_credito.$[0].condicao_credito.valor_bruto": "raw_value",
        "operacoes_credito.$[0].condicao_credito.valor_cliente": "client_value",
        "operacoes_credito.$[0].condicao_credito.valor_financiado": "financed_value",
        "operacoes_credito.$[0].condicao_credito.valor_iof": "iof_value",
        "operacoes_credito.$[0].condicao_credito.valor_liquido": "net_value",
        "operacoes_credito.$[0].condicao_credito.valor_parcela": "installment_value",
        "operacoes_credito.$[0].condicao_credito.valor_solicitado": "requested_value",
    }


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


def test_mapped_dict(highly_nested_data, metadata_credito, target_data, mapping):
    mapper = MapKeys(config=MapKeysConfig(mapping=mapping, preserve_unmapped=False))
    assert mapper.transform(highly_nested_data, metadata_credito)[0] == target_data


def test_unflatted_dict(
    nested_mapping, nested_target_data, highly_nested_data, metadata_credito
):
    mapper = MapKeys(
        config=MapKeysConfig(mapping=nested_mapping, preserve_unmapped=False)
    )
    actual = mapper.transform(highly_nested_data, metadata_credito)[0]
    debug(highly_nested_data)
    debug(nested_target_data)
    debug(actual)
    assert nested_target_data == actual
