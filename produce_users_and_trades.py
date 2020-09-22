#!/usr/bin/env python
'''
Start this app with
> ./start.sh
'''

import os
import ssl

import faust
from faust.types.auth import SASLMechanism

from trade import Trade
from user import User
from general import prevent_freezing
prevent_freezing()

from dotenv import load_dotenv
load_dotenv()


BROKER_USERNAME = os.getenv('BROKER_USERNAME')
BROKER_PASSWORD = os.getenv('BROKER_PASSWORD')


app = faust.App(
    'users-app',
    broker="kafka://" + os.getenv("BROKER_URL"),
    broker_credentials=faust.SASLCredentials(
        username=os.getenv("BROKER_KEY"),
        password=os.getenv("BROKER_SECRET"),
        mechanism="PLAIN",
        ssl_context=ssl.create_default_context(),
    ),

    topic_partitions=12,
    topic_replication_factor=3,
    topic_allow_declare=True,
)
# basic app config: https://faust.readthedocs.io/en/latest/userguide/application.html#application-configuration
# full keyword arguments list: https://faust.readthedocs.io/en/latest/userguide/settings.html#guide-settings
# topic_users = app.topic('users', value_type=User)
topic_users = app.topic('users', value_serializer='json')


# Create users stream
@app.agent(topic_users)
async def users_stream(item):
    # nothing to do here, we have just created a stream
    print("Users stream created")
    pass

how_many_users_to_use=50

# Users Producer - users are constantly registered and update their data :)
@app.timer(interval=1.0)
async def produce_users(app):

    user = {
        "schema": User.schema,
        "payload": User.fake(how_many_users_to_use)
    }

    await users_stream.send(
        value=user,
        key=str(user["payload"]["id"])
    )

    print(f"User created: {user}")


if __name__ == '__main__':
    app.main()
