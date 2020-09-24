# codecs.codec.py
import os

from schema_registry.client import SchemaRegistryClient, schema
from schema_registry.serializers import FaustSerializer
from dotenv import load_dotenv
load_dotenv()

conf = {
    "url": os.getenv("SCHEMA_REGISTRY_ENDPOINT"),
    "basic.auth.credentials.source": "USER_INFO",
    "basic.auth.user.info": os.getenv("SCHEMA_REGISTRY_KEY") + ":" + os.getenv("SCHEMA_REGISTRY_SECRET")
}

# create an instance of the `SchemaRegistryClient`
client = SchemaRegistryClient(conf)

# schema that we want to use. For this example we
# are using a dict, but this schema could be located in a file called avro_user_schema.avsc
avro_user_schema = schema.AvroSchema({
    # schema specs: http://avro.apache.org/docs/current/spec.html
    "type": "record",
    "namespace": "com.ktbst",
    "name": "AvroUsers",
    "fields": [
        {"name": "id", "type": "string"},
        {"name": "name", "type": "string"},
        {"name": "country", "type": "string"},
        {"name": "phone", "type": ["null", "string"], "default": None} # optional nullable field
    ]
})

# avro_trade_schema = schema.AvroSchema({
#     "type": "record",
#     "namespace": "com.example",
#     "name": "AvroTrades",
#     "fields": [
#         {"name": "id", "type": "string"},
#         {"name": "user_id", "type": "string"},
#         {"name": "amount", "type": "string"},
#         {"name": "type", "type": "string"},
#         {"name": "trade_pair", "type": "string"}
#     ]
# })

avro_user_serializer = FaustSerializer(
    client,
    # Kafka Connect can find it automatically if name is: <topicName>-value
    # Subject Name Strategy: https://docs.confluent.io/current/schema-registry/serdes-develop/index.html#sr-schemas-subject-name-strategy
    "users-value",
    avro_user_schema
)
# avro_trade_serializer = FaustSerializer(client, "trades", avro_trade_schema)


# function used to register the codec
def avro_user_codec():
    return avro_user_serializer

from faust.serializers import codecs
codecs.register("avro_users", avro_user_serializer)

# function used to register the codec
# def avro_trade_codec():
#     return avro_trade_serializer
