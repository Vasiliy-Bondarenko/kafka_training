import logging

from app import app
from .models import User
from .codecs import  avro_user_serializer

# page_view_topic = app.topic("page_views", value_type=PageView)
topic_users = app.topic("users", value_type=User)

# page_views = app.Table("page_views", default=int)

logger = logging.getLogger(__name__)

# @app.agent(page_view_topic)
# async def count_page_views(views):
#     async for view in views.group_by(PageView.id):
#         page_views[view.id] += 1
#         logger.info(f"Event received. Page view Id {view.id}")
#
#         yield view



@app.timer(interval=1.0)
async def users_producer():

    user = User.fake(50)

    await topic_users.send(
        value=user,
        key=str(user.id),
        value_serializer=avro_user_serializer
    )

    print(f"User created: {user}")


@app.agent(topic_users)
async def users_consumer(events):
    async for event in events:
        logger.info(event)

        yield event
