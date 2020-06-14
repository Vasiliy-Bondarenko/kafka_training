Watch https://www.youtube.com/watch?v=06iRM1Ghr1k  
And this https://www.youtube.com/watch?v=JalUUBKdcA0


> Docker memory is allocated minimally at 8 GB. When using Docker Desktop for Mac, the default Docker memory allocation is 2 GB. You can change the default allocation to 8 GB in Docker > Preferences > Advanced.

- run `docker-compose up -d`  
- `docker-compose ps` - make sure all services are running  
- if not - restart with `docker-compose stop && docker-compose up -d`
- control with `docker-compose logs --tail=100 -f control-center`
- open in the browser [control center](http://localhost:9021/clusters) - it may take some time to start
- wait for 1 healthy cluster to appear

Congrats! You have a running Kafka cluster. 

- run `docker-compose exec app bash`
- to produce a few messages run  
`python ./producer.py -f ./librdkafka.config -t test1`


expected result:
```
Topic test1 created
Producing record: alice {"count": 0}
Producing record: alice {"count": 1}
Producing record: alice {"count": 2}
Producing record: alice {"count": 3}
Producing record: alice {"count": 4}
Producing record: alice {"count": 5}
Producing record: alice {"count": 6}
Producing record: alice {"count": 7}
Producing record: alice {"count": 8}
Producing record: alice {"count": 9}
Produced record to topic test1 partition [0] @ offset 0
Produced record to topic test1 partition [0] @ offset 1
Produced record to topic test1 partition [0] @ offset 2
Produced record to topic test1 partition [0] @ offset 3
Produced record to topic test1 partition [0] @ offset 4
Produced record to topic test1 partition [0] @ offset 5
Produced record to topic test1 partition [0] @ offset 6
Produced record to topic test1 partition [0] @ offset 7
Produced record to topic test1 partition [0] @ offset 8
Produced record to topic test1 partition [0] @ offset 9
10 messages were produced to topic test1!
```

to consume a few messages run  
`python ./consumer.py -f ./librdkafka.config -t test1` 


expected result:
```
Waiting for message or event/error in poll()
Waiting for message or event/error in poll()
Waiting for message or event/error in poll()
Consumed record with key b'alice' and value b'{"count": 0}',                       and updated total count to 0
Consumed record with key b'alice' and value b'{"count": 1}',                       and updated total count to 1
Consumed record with key b'alice' and value b'{"count": 2}',                       and updated total count to 3
Consumed record with key b'alice' and value b'{"count": 3}',                       and updated total count to 6
Consumed record with key b'alice' and value b'{"count": 4}',                       and updated total count to 10
Consumed record with key b'alice' and value b'{"count": 5}',                       and updated total count to 15
Consumed record with key b'alice' and value b'{"count": 6}',                       and updated total count to 21
Consumed record with key b'alice' and value b'{"count": 7}',                       and updated total count to 28
Consumed record with key b'alice' and value b'{"count": 8}',                       and updated total count to 36
Consumed record with key b'alice' and value b'{"count": 9}',                       and updated total count to 45
Waiting for message or event/error in poll()
Waiting for message or event/error in poll()
Waiting for message or event/error in poll()
```

this was a demo from https://github.com/confluentinc/examples/tree/master/clients/cloud/python

now let's make something ourselves.  
`cd evenodd`

update `producer.py` and make an endless loop producing random numbers every 0.1 second and mark them even or odd.

it can be json records like 
```
{
    "count": number,
    "odd_or_even": odd_or_even(number)
}
```
run the script and let it produce the stream of data into new topic `evenodd`
`python ./producer.py -f ./librdkafka.config -t evenodd`

let the script run in the background

consume only even numbers and calculate running avg. 
print out to the terminal running avg.

run with `python ./consumer.py -f ./librdkafka.config -t evenodd`
 
observe how it will approach 50.

log should look similar to
```
avg: 49.94431348349275 after 567175 items processed
avg: 49.944243056828924 after 567176 items processed
avg: 49.94421318212833 after 567177 items processed
avg: 49.944139229659825 after 567178 items processed
avg: 49.944056461892984 after 567179 items processed
avg: 49.943993088613844 after 567180 items processed
```

- stop the producer
- look how consumer will stop receiving new data, but continue waiting
- update producer to generate random numbers from 0 to 1000
- run it again
- look how producer will pick up new data and avg number start to grow

Now you implemented basic statistical real-time metric and observed how it is fluctuating from  "normal" average value. 

Imagine this producer being trades stream from an exchange.  
Resulting metrics can be displayed on some dashboard - let's say it can be average trade amount, or execution time, etc.
