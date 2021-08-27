import json
from typing import Any, Tuple
from collections import MutableMapping


def convert_flatten(d, parent_key='', sep='.'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k

        if isinstance(v, MutableMapping):
            items.extend(convert_flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


def map_keys(
        data: dict[str, Any], mapping: dict[str, str], preserve_unmapped: bool = True
) -> dict[str, Any]:
    match_result = {}
    data_enrich = convert_flatten(data)

    for map_key, map_value in mapping.items():
        map_value = map_value.replace("*", "")
        splited = map_value.split(".")
        new_query = []
        normal_string = []
        for v in splited:
            if v.isnumeric():
                new_query.append(".".join(normal_string))
                normal_string = []
            normal_string.append(v)

        new_map_value = [v for v in splited if v.isnumeric()]

    if preserve_unmapped:
        for unmapped in (set(data_enrich.keys()) - set(mapping.values())):
            match_result[unmapped] = data_enrich[unmapped]

    return match_result


if __name__ == "__main__":
    data_ = {
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
                    "tipo": "FISICO"
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
                    "digito_conta": "1"
                }
            ]
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
                    "despesas": [],
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
                    "refinanciamentos": []
                }
            }
        ]
    }
    mapping_ = {
        "cpf": "cliente.cpf",
        "ppe": "cliente.pessoa_politicamente_exposta",
        "city": "cliente.enderecos.*0.cidade",
        "name": "cliente.nome",
        "email": "cliente.email",
        "optin": "cliente.opt_in",
        "phone": "cliente.telefone",
        "state": "cliente.enderecos.*0.estado",
        "method": "operacoes_credito.*0.condicao_credito.metodo",
        "address": "cliente.enderecos.*0.logradouro",
        "deadline": "operacoes_credito.*0.condicao_credito.prazo",
        "org_code": "cliente.codigo_orgao",
        "utm_term": "utm_term",
        "zip_code": "cliente.enderecos.*0.cep",
        "iof_value": "operacoes_credito.*0.condicao_credito.valor_iof",
        "net_value": "operacoes_credito.*0.condicao_credito.valor_liquido",
        "raw_value": "operacoes_credito.*0.condicao_credito.valor_bruto",
        "birth_date": "cliente.data_nascimento",
        "utm_medium": "utm_medium",
        "utm_source": "utm_source",
        "bank_number": "cliente.dados_bancarios.*0.numero_banco",
        "nationality": "cliente.nacionalidade",
        "utm_content": "utm_content",
        "address_type": "cliente.enderecos.*0.tipo",
        "client_value": "operacoes_credito.*0.condicao_credito.valor_cliente",
        "lp_form_code": "creditoconsignado_lp_ultimo_passo_form",
        "neighborhood": "cliente.enderecos.*0.bairro",
        "product_code": "operacoes_credito.*0.condicao_credito.codigo_produto",
        "reason_error": "motivo_erro",
        "utm_campaign": "utm_campaign",
        "bank_ag_digit": "cliente.dados_bancarios.*0.digito_agencia",
        "expenses_code": "operacoes_credito.*0.condicao_credito.despesas.*0.codigo",
        "expenses_type": "operacoes_credito.*0.condicao_credito.despesas.*0.tipo",
        "last_due_date": "operacoes_credito.*0.condicao_credito.ultimo_vencimento",
        "address_number": "cliente.enderecos.*0.numero",
        "bank_ag_number": "cliente.dados_bancarios.*0.numero_agencia",
        "expenses_group": "operacoes_credito.*0.condicao_credito.despesas.*0.grupo",
        "financed_value": "operacoes_credito.*0.condicao_credito.valor_financiado",
        "first_due_date": "operacoes_credito.*0.condicao_credito.primeiro_vencimento",
        "marital_status": "cliente.estado_civil",
        "monthly_income": "cliente.renda_mensal",
        "annual_cet_rate": "operacoes_credito.*0.condicao_credito.taxa_cet_anual",
        "document_number": "cliente.numero_documento",
        "requested_value": "operacoes_credito.*0.condicao_credito.valor_solicitado",
        "consigned_margin": "cliente.valor",
        "monthly_cet_rate": "operacoes_credito.*0.condicao_credito.taxa_cet_mensal",
        "bank_account_type": "cliente.dados_bancarios.*0.tipo_conta",
        "benefit_type_code": "cliente.codigo_tipo_beneficio",
        "expenses_financed": "operacoes_credito.*0.condicao_credito.despesas.*0.financiada",
        "expenses_included": "operacoes_credito.*0.condicao_credito.despesas.*0.inclusa",
        "installment_value": "operacoes_credito.*0.condicao_credito.valor_parcela",
        "bank_account_digit": "cliente.dados_bancarios.*0.digito_conta",
        "expenses_mandatory": "operacoes_credito.*0.condicao_credito.despesas.*0.obrigatoria",
        "bank_account_number": "cliente.dados_bancarios.*0.numero_conta",
        "product_description": "operacoes_credito.*0.condicao_credito.descricao_produto",
        "expenses_item_number": "operacoes_credito.*0.condicao_credito.despesas.*0.numero_item",
        "financing_table_code": "operacoes_credito.*0.condicao_credito.codigo_tabela_financiamento",
        "annual_reference_rate": "operacoes_credito.*0.condicao_credito.taxa_referencia_anual",
        "document_emission_date": "cliente.data_emissao_documento",
        "expenses_maximum_value": "operacoes_credito.*0.condicao_credito.despesas.*0.valor_maximo",
        "expenses_minimum_value": "operacoes_credito.*0.condicao_credito.despesas.*0.valor_minimo",
        "monthly_reference_rate": "operacoes_credito.*0.condicao_credito.taxa_referencia_mensal",
        "preferencial_enrollment": "cliente.matricula_preferencial",
        "expenses_caculated_value": "operacoes_credito.*0.condicao_credito.despesas.*0.valor_calculado",
        "annual_appropriation_rate": "operacoes_credito.*0.condicao_credito.taxa_apropriacao_anual",
        "monthly_appropriation_rate": "operacoes_credito.*0.condicao_credito.taxa_apropriacao_mensal",
        "financing_table_description": "operacoes_credito.*0.condicao_credito.descricao_tabela_financiamento",
        "expenses_changeable_default_value": "operacoes_credito.*0.condicao_credito.despesas.*0.valor_padrao_mutavel"
    }
    mapped = map_keys(data_, mapping_, preserve_unmapped=False)
    print(mapped)
