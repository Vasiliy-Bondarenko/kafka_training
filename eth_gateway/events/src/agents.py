import logging
import os

from app import app
from faust.web import Request, Response, View
from src.models.EthEvent import EthEvent

logger = logging.getLogger(__name__)

# !!! uncomment for development only !!!
# from src.schema_registry_client import schemaRegistryClient
# schemaRegistryClient.delete_subject("eth_events-value")

topic_eth_events = app.topic("eth_events", value_type=EthEvent)
EthEvent.init_serializer()

@app.page('/events')
class counter(View):
    async def get(self, request: Request) -> Response:
        logger.info("received GET call")
        logger.info(request.json())
        return self.json({"method": "get"})

    async def post(self, request: Request) -> Response:
        if 'x-api-key' not in request.headers or request.headers['x-api-key'] != os.getenv("ETH_GATEWAY_EVENTS_ENDPOINT_AUTH_KEY"):
            logger.warning("got a non-authorized call")
            return self.error(status=401, reason="Not authorized")

        logger.info("received POST call")
        events_array = await request.json()
        for raw_event in events_array:
            event = EthEvent.decode(raw_event)
            await topic_eth_events.send(
                value=event,
                key=event.transactionHash, # may be change later to customers or accounts to keep the order
            )
        logger.info(f"Confirming {len(events_array)} events received")
        return self.json({"status": "ok"})
