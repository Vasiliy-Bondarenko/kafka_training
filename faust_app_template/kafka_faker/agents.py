import logging

from app import app
from kafka_faker.models.LogItem import LogItem
# from .codecs import  avro_user_serializer


# page_view_topic = app.topic("page_views", value_type=PageView)
topic_logs = app.topic("logs", value_type=LogItem)

# page_views = app.Table("page_views", default=int)

logger = logging.getLogger(__name__)

# @app.agent(page_view_topic)
# async def count_page_views(views):
#     async for view in views.group_by(PageView.id):
#         page_views[view.id] += 1
#         logger.info(f"Event received. Page view Id {view.id}")
#
#         yield view

log_item_serializer = LogItem.init_serializer()

@app.timer(interval=1.0)
async def logs_producer():
    log_item = LogItem.fake()

    await topic_logs.send(
        value=log_item,
        key=str(log_item.customer_id),
        value_serializer=log_item_serializer
    )

    print(f"LogItem created: {log_item}")


@app.agent(topic_logs)
async def logs_consumer(events):
    async for event in events:
        logger.info("Received event: ")
        logger.info(event)
        yield event
