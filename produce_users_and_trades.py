#!/usr/bin/env python
import faust

from trade import Trade
from user import User
from general import prevent_freezing
prevent_freezing()

'''
Start this app with 
> faust -A produce_users_and_trades worker -l info --without-web
'''

# basic app config: https://faust.readthedocs.io/en/latest/userguide/application.html#application-configuration
# full keyword arguments list: https://faust.readthedocs.io/en/latest/userguide/settings.html#guide-settings
app = faust.App(
    'users-app',
    broker='kafka://broker:29092',
    topic_partitions=12,
)
topic_users = app.topic('users', value_type=User)
topic_trades = app.topic('trades', value_type=Trade)

# FIXME: create topic with 8 partitions MANUALLY or with some other method like confluent kafka client.
# Faust DOEST NOT create "external" topics: https://faust.readthedocs.io/en/latest/userguide/settings.html#topic-allow-declare

# Create users stream
@app.agent(topic_users)
async def users_stream(item):
    # nothing to do here, we have just created a stream
    print("Users stream created")
    pass

# Create trades stream
@app.agent(topic_trades)
async def trades_stream(item):
    # nothing to do here, we have just created a stream
    print("Trades stream created")
    pass

how_many_users_to_use=2

# Users Producer - users are constantly registered and update their data :)
@app.timer(interval=1.0)
async def produce_users(app):
    user = User.fake(id_up_to=how_many_users_to_use)
    print(f"Producing user: {user}")
    await users_stream.send(
        value=user,
        key=str(user.id),
    )

# Trades Producer
@app.timer(interval=0.25)
async def produce_trades(app):
    trade = Trade.fake(users_id_up_to=how_many_users_to_use)
    print(f"Producing trade: {trade}")
    await trades_stream.send(
        value=trade,
        key=str(trade.user_id),
    )


if __name__ == '__main__':
    app.main()
