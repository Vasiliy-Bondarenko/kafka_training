import os
from schema_registry.client import SchemaRegistryClient, schema
from schema_registry.client.errors import ClientError
from dotenv import load_dotenv
from schema_registry.serializers import FaustSerializer

load_dotenv()


conf = {
    "url": os.getenv("SCHEMA_REGISTRY_ENDPOINT"),
    "basic.auth.credentials.source": "USER_INFO",
    "basic.auth.user.info": os.getenv("SCHEMA_REGISTRY_KEY") + ":" + os.getenv("SCHEMA_REGISTRY_SECRET")
}


# create an instance of the `SchemaRegistryClient`
client = SchemaRegistryClient(conf)

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

avro_user_serializer = FaustSerializer(client, "users", avro_user_schema)

try:
    r = client.get_subjects()
    raise Exception(r)


except ClientError as e:
    print(e.http_code)

