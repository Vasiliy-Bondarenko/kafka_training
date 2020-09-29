import logging
import os

from app import app
from src.models.LogItem import LogItem
# from .codecs import  avro_user_serializer


eth_transaction_requests_topic = app.topic(os.getenv("KALEIDO_SUBMIT_TOPIC"), value_serializer='json')
topic_logs = app.topic("logs", value_type=LogItem)

# page_views = app.Table("page_views", default=int)

logger = logging.getLogger(__name__)

@app.timer(interval=1.0)
async def send_transfer():
    from faker import Faker
    fake = Faker()
    id=fake.uuid4()
    contract_address = "0x0cc82c5d228e197cc6cf57f5965dadf0280f2116"
    contract_deployed_from = "0xdf1a197b098105bb296b4e91e9467fe2df155fe2"
    recipient = "0x4222e15afd8807782885a0af94770619fdbdce7d"

    await eth_transaction_requests_topic.send(value={
        "from": contract_deployed_from,
        "gas": 0,
        "gasPrice": 0,
        "headers": {
            "id": id,
            "type": "SendTransaction"
        },
        "method": {
            "inputs": [
                {
                    "name": "recipient",
                    "type": "address"
                },
                {
                    "name": "amount",
                    "type": "uint256"
                }
            ],
            "name": "transfer",
            "outputs": [
                {
                    "name": "",
                    "type": "bool"
                }
            ],
            "stateMutability": "nonpayable",
            "type": "function"
        },
        "params": [
            recipient,
            "8789789"
        ],
        "to": contract_address,
        "value": 0
    })
    print(f"Tx with id {id} produced")

log_item_serializer = LogItem.init_serializer()

# @app.timer(interval=1.0)
# async def logs_producer():
#     log_item = LogItem.fake()
#
#     await topic_logs.send(
#         value=log_item,
#         key=str(log_item.customer_id),
#         value_serializer=log_item_serializer
#     )
#
#     print(f"LogItem created: {log_item}")


@app.agent(topic_logs)
async def logs_consumer(events):
    async for event in events:
        logger.info("Received event: ")
        logger.info(event)
        yield event
