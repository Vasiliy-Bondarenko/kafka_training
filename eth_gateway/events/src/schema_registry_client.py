import os

from dotenv import load_dotenv
from schema_registry.client import SchemaRegistryClient

load_dotenv()

conf = {
    "url": os.getenv("SCHEMA_REGISTRY_ENDPOINT"),
    "basic.auth.credentials.source": "USER_INFO",
    "basic.auth.user.info": os.getenv("SCHEMA_REGISTRY_KEY") + ":" + os.getenv("SCHEMA_REGISTRY_SECRET")
}

# create an instance of the `SchemaRegistryClient`
schemaRegistryClient = SchemaRegistryClient(conf)
