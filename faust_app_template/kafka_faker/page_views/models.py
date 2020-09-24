import faust
from schema_registry.client import schema
from schema_registry.serializers import FaustSerializer
from kafka_faker.schema_registry_client import schemaRegistryClient
from faust.serializers import codecs


class PageView(faust.Record):
    id: str
    user: str


from faker import Faker

fake = Faker()


class User(faust.Record, serializer='avro_users'):
    id: str
    name: str
    country: str
    phone: str

    @classmethod
    def init_serializer(cls):
        serializer = FaustSerializer(
            schemaRegistryClient,
            # Kafka Connect can find it automatically if name is: <topicName>-value
            # Subject Name Strategy: https://docs.confluent.io/current/schema-registry/serdes-develop/index.html#sr-schemas-subject-name-strategy
            "users-value",
            cls.schema()
        )

        codecs.register("avro_users", serializer)

        return serializer

    @staticmethod
    def schema():
        return schema.AvroSchema({
            # schema specs: http://avro.apache.org/docs/current/spec.html
            "type": "record",
            "namespace": "com.ktbst",
            "name": "AvroUsers",
            "fields": [
                {"name": "id", "type": "string"},
                {"name": "name", "type": "string"},
                {"name": "country", "type": "string"},
                {"name": "phone", "type": ["null", "string"], "default": None},  # optional nullable field
                {"name": "address", "type": ["null", "string"], "default": None}  # optional nullable field
            ]
        })

    @staticmethod
    def fake(id_up_to=10):
        return User(
            # faker docs: https://faker.readthedocs.io/en/master/index.html
            id=str(fake.random_int(1, id_up_to)),
            name=fake.name(),
            country=fake.country(),
            phone=fake.phone_number()
        )
