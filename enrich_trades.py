#!/usr/bin/env python
import faust
# Patch mode to ensure we crash
# Issue: https://github.com/robinhood/faust/issues/484
import mode

from enriched_trade import EnrichedTrade
from trade import Trade
from user import User
from general import prevent_freezing

prevent_freezing()

'''
Start this app with 
> faust -A enrich_trades worker -l info --without-web
'''

app = faust.App(
    'enrich_trades_with_users_app',
    broker='kafka://broker:29092',
    topic_partitions=12,
)
topic = app.topic('users', value_type=User)
topic_trades = app.topic('trades', value_type=Trade)
topic_enriched_trades = app.topic('enriched_trades', value_type=EnrichedTrade)
users_table = app.Table('users_table', default=None)


# Create users table
@app.agent(topic)
async def create_users_table(users):
    global users_table
    # stream = users.group_by(key=User.id)
    async for user in users:
        users_table[user.id] = user
        print(f"Updated user in a users_table: {user.id}: {user.name}")


# Create enriched trades stream
@app.agent(topic_enriched_trades)
async def enriched_trades_stream(enriched_trades):
    print("Enriched trades stream created")
    async for trade in enriched_trades:
        print(f"Enriched trade user: {trade.user}")


# Create trades stream
@app.agent(topic_trades, sink=[topic_enriched_trades])
async def trades_stream(trades):
    print("Trades stream created")
    async for trade in trades:
        if str(trade.user_id) not in users_table:
            print(f"no user found for id {trade.user_id} table len: {len(users_table)}")
            continue

        user = users_table[str(trade.user_id)]
        yield EnrichedTrade(
            user_id=trade.user_id,
            user=user,
            id=trade.id,
            amount=trade.amount,
            type=trade.type,
            trade_pair=trade.trade_pair,
        )  # dump result into sink topic


if __name__ == '__main__':
    app.main()
