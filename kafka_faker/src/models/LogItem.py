import faust
from schema_registry.client import schema
from schema_registry.serializers import FaustSerializer
from src.schema_registry_client import schemaRegistryClient
from faust.serializers import codecs

from faker import Faker

fake = Faker()


class LogItem(faust.Record, serializer='log_item'):
    source: str
    severity: str
    customer_id: int
    account_id: int
    transaction_id: int
    message: str

    _schema_subject = "logs-value"

    @classmethod
    def init_serializer(cls):
        serializer = FaustSerializer(
            schemaRegistryClient,
            # Kafka Connect can find it automatically if name is: <topicName>-value
            # Subject Name Strategy: https://docs.confluent.io/current/schema-registry/serdes-develop/index.html#sr-schemas-subject-name-strategy
            cls._schema_subject,
            cls.schema()
        )

        codecs.register("log_item", serializer)

        return serializer

    @classmethod
    def schema(cls):
        schema_json = {
            # schema specs: http://avro.apache.org/docs/current/spec.html
            "type": "record",
            "namespace": "com.ktbst",
            "name": "LogItem",
            "fields": [
                {"name": "message", "type": "string"},
                {"name": "source", "type": "string"},
                {"name": "severity", "type": {"type": "enum", "name": "severity", "symbols": cls.severity_values()}},
                {"name": "customer_id", "type": ["null", "int"], "default": None},
                {"name": "account_id", "type": ["null", "int"], "default": None},
                {"name": "transaction_id", "type": ["null", "int"], "default": None},
            ]
        }
        return schema.AvroSchema(schema_json)

    @classmethod
    def severity_values(cls):
        return ["FATAL", "ERROR", "WARN", "INFO", "DEBUG", "TRACE"]

    @classmethod
    def fake(cls):
        return LogItem(
            # faker docs: https://faker.readthedocs.io/en/master/index.html
            message=fake.sentence(),
            source=fake.random_element(elements=('ISP Portal', 'ERP Client', 'ISP API', 'ISP Scheduler', 'Event processor', 'Ethereum Gateway')),
            severity=fake.random_element(elements=cls.severity_values()),
            customer_id=fake.random_int(1, 1000),
            account_id=fake.random_int(1, 5000),
            transaction_id=fake.random_int(1, 50000),
        )
