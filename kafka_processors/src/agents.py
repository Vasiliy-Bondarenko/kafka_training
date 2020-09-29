import logging

logger = logging.getLogger(__name__)

import os

from app import app

from src.models.EthTxRequest import EthTxRequest
from src.models.EthTxResponse import EthTxResponse
from src.schema_registry_client import schemaRegistryClient

# !!! uncomment for development only !!!
# schemaRegistryClient.delete_subject("eth_transactions_receive-value")
# schemaRegistryClient.delete_subject("eth_transactions_submit")

# initialize topics
eth_tx_submit_topic = app.topic(os.getenv("KALEIDO_SUBMIT_TOPIC"), value_serializer='json')
eth_tx_receive_topic = app.topic(os.getenv("KALEIDO_RECEIVE_TOPIC"), value_serializer='json')
eth_tx_submit_avro_topic = app.topic("eth_transactions_submit", value_type=EthTxRequest)
eth_tx_receive_avro_topic = app.topic("eth_transactions_receive", value_type=EthTxResponse)

# initialize model serializers
EthTxRequest.init_serializer()
EthTxResponse.init_serializer()

# takes messages from json topic and pushes to avro topic
@app.agent(eth_tx_submit_topic, concurrency=12)
async def eth_tx_submit_proxy(events):
    async for event in events:
        ethTxRequest = EthTxRequest.decode(event)
        logger.info(f"Received transaction: {ethTxRequest.id}")
        await eth_tx_submit_avro_topic.send(value=ethTxRequest)

# takes messages from json topic and pushes to avro topic
@app.agent(eth_tx_receive_topic, concurrency=12)
async def eth_tx_receive_proxy(events):
    async for event in events:
        ethTxResponse = EthTxResponse.decode(event)
        logger.info(f"Received transaction response: {ethTxResponse.id}")
        await eth_tx_receive_avro_topic.send(value=ethTxResponse)
