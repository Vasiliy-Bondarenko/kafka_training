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
> faust -A users_consume_faust worker -l info --without-web
'''


app = faust.App('users-consumer-app-2', broker='kafka://broker:29092')
topic = app.topic('users', value_type=User)
new_users_by_country = app.Table('new_users_by_country', default=int)

def country_filter(user: User) -> bool:
    return user.country.startswith("U") \
           or user.country.startswith("R") \
           or user.country.startswith("A")

@app.agent(topic)
async def process(users):
    # - take initial stream of users
    # - filter only users with countries starting with U or R or A
    # - repartition by user's id. note: id should be of type string to avoid problems.
    stream = users\
        .filter(country_filter)\
        .group_by(key=User.id)\
        .group_by(key=User.country)

    async for user in stream:
        new_users_by_country[user.country] += 1
        print(f"{user.id}: {user.name}")
        # print(f"{user.country}: {new_users_by_country[user.country]}")


if __name__ == '__main__':
    app.main()
