import random
import uuid

from faker import Faker

from src.the_flash.models.mat_events import ServiceLetter

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


def letter_gen(number: int) -> ServiceLetter:
    for _ in range(number):
        yield ServiceLetter.parse_obj(dict(
            event_trace=str(uuid.uuid4()),
            mat_id="field_translator",
            data=data_factory(),
            config=config_factory(),
            index_in_flow=0
        ))
