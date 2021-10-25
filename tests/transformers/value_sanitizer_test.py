from transformer.transformers.value_sanitizer import (
    ValueSanitizer,
    ValueSanitizerConfig,
)


def test_aggregate_keys():
    data = {
        "id": 1645687,
        "email_1": "NOME#gmail.com",
        "email_2": "NOME#gmail.com",
        "e": {"a": "s", "g": [1, 2]},
        "f": [1, 2, 3, 4],
    }
    target_data = {
        "id": 1645687,
        "email_1": "nome@decode.buzz",
        "email_2": "nome@decode.buzz",
        "e": {"a": "s", "g": [1, 2]},
        "f": [1, 2, 3, 4],
    }

    sanitizer = ValueSanitizer(
        config=ValueSanitizerConfig(
            key_pattern="^(email_).*",
            substitution_pattern="#gmail.com",
            sub_string="@decode.buzz",
            string_methods=["lower"],
        )
    )
    transformed_data, _ = sanitizer.transform(data, {})
    assert target_data == transformed_data


def test_cpf_mask_remover():
    data = {
        "id": 1645687,
        "cpf": "123.456.789-01",
        "e": {"a": "s", "g": [1, 2]},
        "f": [1, 2, 3, 4],
    }
    target_data = {
        "id": 1645687,
        "cpf": "12345678901",
        "e": {"a": "s", "g": [1, 2]},
        "f": [1, 2, 3, 4],
    }
    sanitizer = ValueSanitizer(
        config=ValueSanitizerConfig(key_pattern="cpf", substitution_pattern="[^0-9]")
    )
    transformed_data, _ = sanitizer.transform(data, {})
    assert target_data == transformed_data
