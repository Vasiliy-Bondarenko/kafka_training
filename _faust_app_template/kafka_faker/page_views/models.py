import faust


class PageView(faust.Record):
    id: str
    user: str


from faker import Faker

fake = Faker()

class User():
    schema = {
        "type": "struct",
        "optional": False,
        "version": 1,
        "fields": [
            {
                "field": "id",
                "type": "string",
                "optional": False
            },
            {
                "field": "name",
                "type": "string",
                "optional": False
            },
            {
                "field": "country",
                "type": "string",
                "optional": True
            }
        ]
    }

    @staticmethod
    def fake(id_up_to=10):
        return {
            "id": str(fake.random_int(1, id_up_to)),
            "name": fake.name(),
            "country": fake.country(),
        }
