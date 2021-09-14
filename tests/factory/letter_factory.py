import random
from faker import Faker

fake = Faker()


def data_factory():
    lying_data = {
        "Name": fake.name(),
        "Address": fake.address(),
        "Email": fake.email(),
        "Country": fake.country(),
        "Age": random.randint(10, 50)
    }
    return lying_data


def config_factory():
    lying_data = data_factory()
    config = {
        "mapping": {k: k.lower() for k, v in lying_data.items()},
        "preserve_unmapped": random.choice([True, False])
    }
    return config
