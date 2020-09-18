#!/usr/bin/env python
import faust

from trade import Trade
from user import User
from general import prevent_freezing
prevent_freezing()


'''
Start this app with 
> ./start.sh
'''

# basic app config: https://faust.readthedocs.io/en/latest/userguide/application.html#application-configuration
# full keyword arguments list: https://faust.readthedocs.io/en/latest/userguide/settings.html#guide-settings
app = faust.App(
    'users-app',
    broker='kafka://broker:29092',
    topic_partitions=12,
)
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

    print(f"Producing user: {user['payload']}")

    await users_stream.send(
        value=user,
        key=str(user["payload"]["id"]),
    )


if __name__ == '__main__':
    app.main()
