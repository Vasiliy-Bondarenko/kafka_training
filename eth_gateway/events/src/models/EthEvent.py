import json
import os

from faker import Faker
from src.models.BaseModel import BaseModel

fake = Faker()


class EthEvent(BaseModel, serializer='eth_event'):
    address: str
    blockNumber: int
    transactionIndex: str
    transactionHash: str
    data: str
    subId: str
    signature: str
    logIndex: int

    _serializer = 'eth_event'
    _schema_subject = f"eth_events-value"
    _schema = {
        # schema specs: http://avro.apache.org/docs/current/spec.html
        "type": "record",
        "namespace": "com.ktbst",
        "name": "EthEvent",
        "fields": [
            {"name": "address", "type": "string"},
            {"name": "blockNumber", "type": "int"},
            {"name": "transactionIndex", "type": "string"},
            {"name": "transactionHash", "type": "string"},
            {"name": "data", "type": "string"},
            {"name": "subId", "type": "string"},
            {"name": "signature", "type": "string"},
            {"name": "logIndex", "type": "int"},
        ]
    }

    @classmethod
    def decode(cls, event):
        '''
        Creates EthEvent model from json

        Event json example:
        {
          "address": "0x0Cc82c5d228e197cc6cF57F5965daDF0280f2116",
          "blockNumber": "684",
          "transactionIndex": "0x1",
          "transactionHash": "0x36e294dcb2451dd09b82454b41cf4889d99bc4bc51748f8af519439dc7c81acf",
          "data": {
            "from": "0xdf1a197b098105bb296b4e91e9467fe2df155fe2",
            "to": "0x4222e15afd8807782885a0af94770619fdbdce7d",
            "value": "1"
          },
          "subId": "sb-e98a6952-a24c-4d11-4aa3-e481ba00813b",
          "signature": "Transfer(address,address,uint256)",
          "logIndex": "400"
        }
        '''

        return cls(
            signature=event["signature"],
            data=json.dumps(event["data"]),
            transactionHash=event["transactionHash"],
            address=event["address"],
            blockNumber=int(event["blockNumber"]),
            transactionIndex=event["transactionIndex"],
            subId=event["subId"],
            logIndex=int(event["logIndex"]),
        )

