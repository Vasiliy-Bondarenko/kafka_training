import logging
import os

from app import app
from src.models.LogItem import LogItem
# from .codecs import  avro_user_serializer


eth_transaction_requests_topic = app.topic(os.getenv("KALEIDO_SUBMIT_TOPIC"), value_serializer='json')
topic_logs = app.topic("logs", value_type=LogItem)

# page_views = app.Table("page_views", default=int)

logger = logging.getLogger(__name__)

counter = 0

@app.timer(interval=1.0)
async def send_transfer():
    global counter
    from faker import Faker
    fake = Faker()


    how_many = 1000
    for n in range(1, how_many):
        counter=counter+1
        id=fake.uuid4()
        contract_address = "0x0cc82c5d228e197cc6cf57f5965dadf0280f2116"
        contract_deployed_from = "0xdf1a197b098105bb296b4e91e9467fe2df155fe2"
        recipient = "0x4222e15afd8807782885a0af94770619fdbdce7d"
        function_name = fake.random_element(["transfer", "transfer", "transfer", "not_existing_function_name"])

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
                "name": function_name,
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
                "1"
            ],
            "to": contract_address,
            "value": 0
        })
        # print(f"Tx {counter} with id {id} produced")

    print(f"{how_many} txs created")

log_item_serializer = LogItem.init_serializer()

@app.timer(interval=1.0)
async def logs_producer():
    log_item = LogItem.fake()

    how_many = 3
    for n in range(1, how_many):
        await topic_logs.send(
            value=log_item,
            key=str(log_item.customer_id),
            value_serializer=log_item_serializer
        )

        # print(f"LogItem created: {log_item}")

    print(f"{how_many} LogItems created")


# @app.agent(topic_logs)
# async def logs_consumer(events):
#     async for event in events:
#         logger.info("Received event: ")
#         logger.info(event)
#         yield event
