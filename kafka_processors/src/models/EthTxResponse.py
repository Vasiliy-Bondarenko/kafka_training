import json
import os

from faker import Faker
from src.models.BaseModel import BaseModel

fake = Faker()


class EthTxResponse(BaseModel, serializer='eth_tx_response'):
    id: str
    from_address: str
    tx: str
    status: int
    tx_hash: str

    _serializer = 'eth_tx_response'
    _schema_subject = f"eth_transactions_receive-value"
    _schema = {
        # schema specs: http://avro.apache.org/docs/current/spec.html
        "type": "record",
        "namespace": "com.ktbst",
        "name": "EthTxResponse",
        "fields": [
            {"name": "id", "type": "string"},
            {"name": "from_address", "type": "string"},
            {"name": "tx_hash", "type": "string"},
            {"name": "status", "type": "int"},
            {"name": "tx", "type": "string"},
        ]
    }

    @classmethod
    def decode(cls, tx):
        return cls(
            id=tx["headers"]["requestId"],
            from_address=tx["from"],
            status=int(tx["status"]),
            tx_hash=tx["transactionHash"],
            tx=json.dumps(tx),
        )

