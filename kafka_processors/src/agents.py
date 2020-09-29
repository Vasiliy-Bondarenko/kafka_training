import json
import logging
import os

from app import app

from src.models.EthTxRequest import EthTxRequest

eth_tx_submit_topic = app.topic(os.getenv("KALEIDO_SUBMIT_TOPIC"), value_serializer='json')
eth_tx_submit_avro_topic = app.topic("eth_transactions_submit", value_type=EthTxRequest)

logger = logging.getLogger(__name__)
log_item_serializer = EthTxRequest.init_serializer()

# @app.timer(interval=1.0)
# async def send_transfer():
#     await eth_tx_submit_topic.send(value=)
#     print(f"Tx with id {id} produced")


@app.agent(eth_tx_submit_topic)
async def eth_tx_submit_proxy(events):
    async for event in events:
        ethTxRequest = EthTxRequest.decode(event)
        logger.info("Received transaction: ")
        logger.info(ethTxRequest)
        await eth_tx_submit_avro_topic.send(value=ethTxRequest)
        # yield event
        # raise Exception("HERE")

