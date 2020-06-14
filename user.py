import faust
from faker import Faker

fake = Faker()


class User(faust.Record):
    id: str
    name: str
    country: str

    def __str__(self):
        return f"{self.id}: {self.name} from {self.country}"

    @staticmethod
    def fake(id_up_to=10):
        return User(
            id=str(fake.random_int(1, id_up_to)),
            name=fake.name(),
            country=fake.country(),
        )
