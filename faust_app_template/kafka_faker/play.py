import os
from schema_registry.client import SchemaRegistryClient, schema
from schema_registry.client.errors import ClientError
from dotenv import load_dotenv
from schema_registry.serializers import FaustSerializer
from schema_registry_client import schemaRegistryClient
#
# # avro_user_schema = schema.AvroSchema({
# #     "type": "record",
# #     "namespace": "com.example",
# #     "name": "AvroUsers",
# #     "fields": [
# #         {"name": "id", "type": "string"},
# #         {"name": "name", "type": "string"},
# #         {"name": "country", "type": "string"}
# #     ]
# # })
# #
# # avro_user_serializer = FaustSerializer(client, "users-value", avro_user_schema)
#
try:
    r = schemaRegistryClient.delete_subject("users-value")
    raise Exception(r)


except ClientError as e:
    print(e.http_code)
