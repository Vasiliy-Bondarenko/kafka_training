# codecs.codec.py
from schema_registry.client import SchemaRegistryClient, schema
from schema_registry.serializers import FaustSerializer

# create an instance of the `SchemaRegistryClient`
client = SchemaRegistryClient(url="http://schema-registry:8081")

# schema that we want to use. For this example we
# are using a dict, but this schema could be located in a file called avro_user_schema.avsc
avro_user_schema = schema.AvroSchema({
    "type": "record",
    "namespace": "com.example",
    "name": "AvroUsers",
    "fields": [
        {"name": "id", "type": "string"},
        {"name": "name", "type": "string"},
        {"name": "country", "type": "string"}
    ]
})
avro_trade_schema = schema.AvroSchema({
    "type": "record",
    "namespace": "com.example",
    "name": "AvroTrades",
    "fields": [
        {"name": "id", "type": "string"},
        {"name": "user_id", "type": "string"},
        {"name": "amount", "type": "string"},
        {"name": "type", "type": "string"},
        {"name": "trade_pair", "type": "string"}
    ]
})

avro_user_serializer = FaustSerializer(client, "users", avro_user_schema)
avro_trade_serializer = FaustSerializer(client, "trades", avro_trade_schema)


# function used to register the codec
def avro_user_codec():
    return avro_user_serializer

# function used to register the codec
def avro_trade_codec():
    return avro_trade_serializer
