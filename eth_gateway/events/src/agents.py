import logging
from app import app
from faust.web import Request, Response, View

logger = logging.getLogger(__name__)


@app.page('/events/')
class counter(View):
    async def get(self, request: Request) -> Response:
        logger.info("received GET call")
        logger.info(request)
        return self.json({"method": "get"})

    async def post(self, request: Request) -> Response:
        logger.info("received POST call")
        logger.info(request)
        return self.json({"method": "post"})
