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

    await eth_transaction_requests_topic.send(value={
        "from": "0xe2ef28a7ee6aa52286ff73106e2a928ef9203f3d",
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
            "0x4222e15afd8807782885a0af94770619fdbdce7d",
            "1"
        ],
        "to": "0xf3a23e87e5764a2102eb77630e262f4717975c8d",
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
