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


def letter_gen(number: int) -> ServiceLetter:
    for _ in range(number):
        yield ServiceLetter(
            event_trace=str(uuid.uuid4()),
            mat_id="field_translator",
            data=data_factory(),
            config=config_factory(),
            index_in_flow=0
        ).json().encode("utf-8")


def config_factory():
    lying_data = data_factory()
    config = {
        "mapping": {k: k.lower() for k, v in lying_data.items()},
        "preserve_unmapped": random.choice([True, False])
    }
    return config
