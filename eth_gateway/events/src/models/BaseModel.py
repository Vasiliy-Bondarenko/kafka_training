import faust
from faker import Faker
from faust.serializers import codecs
from schema_registry.client import schema
from schema_registry.serializers import FaustSerializer
from src.schema_registry_client import schemaRegistryClient

fake = Faker()


class BaseModel(faust.Record):
    _serializer = None
    _schema_subject = None
    _schema = None


    @classmethod
    def init_serializer(cls):
        if cls._serializer is None:
            raise Exception("Set _serializer property")
        if cls._schema_subject is None:
            raise Exception("Set _schema_subject property")

        serializer = FaustSerializer(
            schemaRegistryClient,
            # Kafka Connect can find it automatically if name is: <topicName>-value
            # Subject Name Strategy: https://docs.confluent.io/current/schema-registry/serdes-develop/index.html#sr-schemas-subject-name-strategy
            cls._schema_subject,
            cls.schema()
        )

        codecs.register(cls._serializer, serializer)

        return serializer

    @classmethod
    def schema(cls):
        if cls._schema is None:
            raise Exception("Set _schema property")

        return schema.AvroSchema(cls._schema)
