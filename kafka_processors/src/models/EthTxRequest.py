import json
import os

from faker import Faker
from src.models.BaseModel import BaseModel

fake = Faker()


class EthTxRequest(BaseModel, serializer='eth_tx_request'):
    id: str
    from_address: str
    tx: str

    _serializer = 'eth_tx_request'
    _schema_subject = f"eth_transactions_submit-value"
    _schema = {
        # schema specs: http://avro.apache.org/docs/current/spec.html
        "type": "record",
        "namespace": "com.ktbst",
        "name": "EthTxRequest",
        "fields": [
            {"name": "id", "type": "string"},
            {"name": "from_address", "type": "string"},
            {"name": "tx", "type": "string"},
        ]
    }

    @classmethod
    def decode(cls, tx):
        return cls(
            id=tx["headers"]["id"],
            from_address=tx["from"],
            tx=json.dumps(tx),
        )

