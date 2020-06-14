#!/usr/bin/env python
import faust
# Patch mode to ensure we crash
# Issue: https://github.com/robinhood/faust/issues/484
import mode

from user import User
from general import prevent_freezing
prevent_freezing()

'''
Start this app with 
> faust -A tx_broadcaster worker -l info --without-web
'''


app = faust.App('tx-broadcaster-app', broker='kafka://broker:29092')
transactions_to_broadcast_topic = app.topic('transactions_to_broadcast', value_type=User)
transactions_to_watch_topic = app.topic('transactions_to_watch', value_type=User) # consumed by Eventeum

@app.agent(transactions_to_broadcast_topic)
async def process(transactions):
    async for transaction in transactions:
        try:
            ok = broadcast(transaction)
            if ok:
                confirm(transaction)
        except AlreadyExists as e:
            confirm(transaction)

def confirm(transaction):
    transaction.ack()
    transactions_to_watch_topic.send(key=transaction.id, value=transaction)

def broadcast(transaction):
    # broadcast with infura/kaleido APIs
    # it can be very thin clients using REST API on Kaleido

    # How do we sign transactions??? https://docs.kaleido.io/kaleido-services/cloudhsm/ - ?
    pass


if __name__ == '__main__':
    app.main()
