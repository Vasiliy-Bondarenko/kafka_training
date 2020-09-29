import json
import os

from faker import Faker
from src.models.BaseModel import BaseModel

fake = Faker()


class EthTxResponse(BaseModel, serializer='eth_tx_response'):
    id: str
    status: str  # "SUCCESS" | "ERROR"
    type: str  # "TransactionFailure" | "TransactionSuccess" | "Error"
    from_address: str
    tx: str
    status: int
    tx_hash: str
    error: str

    _serializer = 'eth_tx_response'
    _schema_subject = f"eth_transactions_receive-value"
    _schema = {
        # schema specs: http://avro.apache.org/docs/current/spec.html
        "type": "record",
        "namespace": "com.ktbst",
        "name": "EthTxResponse",
        "fields": [
            {"name": "id", "type": "string"},
            {"name": "status", "type": "string"},
            {"name": "type", "type": "string"},
            {"name": "error", "type": ["string", "null"], "default": None},
            {"name": "from_address", "type": ["string", "null"], "default": None},
            {"name": "tx_hash", "type": ["string", "null"], "default": None},
            {"name": "tx", "type": "string"},
        ]
    }
    STATUS_SUCCESS = "SUCCESS"
    STATUS_ERROR = "ERROR"

    @classmethod
    def get_status_as_text(cls, tx: dict):
        # https://github.com/Arachnid/EIPs/blob/947e76504373558c1c7655c360a9d02840c539f9/EIPS/eip-draft-returndata.md
        if tx.get("status") == "1":
            return cls.STATUS_SUCCESS
        return cls.STATUS_ERROR

    @classmethod
    def decode(cls, tx):
        # examples of receipts: https://docs.kaleido.io/kaleido-services/ethconnect/receipt-store/
        try:
            return cls(
                id=tx["headers"]["requestId"],
                type=tx["headers"]["type"],
                error=tx.get("errorMessage"),
                from_address=tx.get("from"),
                status=cls.get_status_as_text(tx),
                tx_hash=tx.get("transactionHash"),
                tx=json.dumps(tx),
            )
        except Exception as e:
            raise Exception(f"We,ve got an error processing this transaction: {json.dumps(tx)}\n Error: {e}")
