from typing import Dict

import pytest


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


@pytest.fixture
def highly_nested_data():
    return {
        "id": 1645687,
        "cliente": {
            "nome": "Marli Aparecida Ana das Neves",
            "email": "marliaparecidaanadasneves-77@decode.buzz",
            "telefone": "(63) 36366-1878",
            "cpf": "99915697902",
            "opt_in": True,
            "enderecos": [
                {
                    "cep": "77021-050",
                    "estado": "TO",
                    "cidade": "Palmas",
                    "bairro": "Plano Diretor Sul",
                    "logradouro": "ARSE 32 Alameda 1",
                    "numero": "326",
                    "tipo": "FISICO",
                }
            ],
            "numero_documento": "407941319",
            "data_emissao_documento": "10-02-2000",
            "nacionalidade": "BRASILEIRA",
            "estado_civil": "CASADO",
            "pessoa_politicamente_exposta": False,
            "codigo_orgao": "000501",
            "codigo_tipo_beneficio": 42,
            "data_nascimento": "18-02-1989",
            "matricula_preferencial": "0000000000",
            "renda_mensal": 1000,
            "valor": 100,
            "valor_cliente": 4117.48,
            "valor_parcela": 100,
            "prazo": 84,
            "dados_bancarios": [
                {
                    "tipo_conta": "CONTA_CORRENTE_INDIVIDUAL",
                    "numero_banco": "001",
                    "numero_agencia": "265",
                    "digito_agencia": "4",
                    "numero_conta": "71444",
                    "digito_conta": "1",
                }
            ],
        },
        "creditoconsignado_lp_ultimo_passo_form": 7,
        "codigo_orgao": "000501",
        "operacoes_credito": [
            {
                "condicao_credito": {
                    "sucesso": True,
                    "mensagem_erro": "",
                    "prazo": 84,
                    "metodo": "VALOR_SOLICITADO",
                    "codigo_tabela_financiamento": "703347",
                    "descricao_tabela_financiamento": "INSS_NOV_DIG_NORMAL",
                    "codigo_produto": "000440",
                    "descricao_produto": "INSS - MARGEM",
                    "primeiro_vencimento": "07-10-2021",
                    "ultimo_vencimento": "07-09-2028",
                    "despesas": [
                        {
                            "codigo": 1234,
                            "financiada": "sim",
                            "valor_minimo": 1,
                            "valor_maximo": 2,
                        }
                    ],
                    "taxa_apropriacao_anual": 23.8721,
                    "taxa_apropriacao_mensal": 1.8,
                    "taxa_cet_anual": 25.6687,
                    "taxa_cet_mensal": 1.8957,
                    "taxa_referencia_anual": 24.238,
                    "taxa_referencia_mensal": 1.825,
                    "valor_bruto": 8400,
                    "valor_cliente": 4117.48,
                    "valor_financiado": 4246.6,
                    "valor_solicitado": 4117.48,
                    "valor_iof": 129.12,
                    "valor_liquido": 4117.48,
                    "valor_parcela": 100,
                    "refinanciamentos": [],
                }
            }
        ],
    }
