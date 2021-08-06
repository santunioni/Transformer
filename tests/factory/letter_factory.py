import random


def letter_factory():
    lying_data = {
        "Name": "foo",
        "PHone": random.choice(range(1, 5)),
        "AGE": random.choice(range(1, 80))
    }
    return lying_data


def config_factory():
    lying_data = letter_factory()
    config = {
        "mapping": {k: k.lower() for k, v in lying_data.items()},
        "preserve_unmapped": random.choice([True, False])
    }
    return config
