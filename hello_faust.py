#!/usr/bin/env python
import faust

'''
The example application starts two tasks: one is processing a stream, the other is a background thread sending events to that stream. In a real-life application, your system will publish events to Kafka topics that your processors can consume from, and the background thread is only needed to feed data into our example.
'''

class Greeting(faust.Record):
    from_name: str
    to_name: str

app = faust.App('hello-app', broker='kafka://broker:29092')
topic = app.topic('hello-topic', value_type=Greeting)

@app.agent(topic)
async def hello(greetings):
    async for greeting in greetings:
        print(f'Hello from {greeting.from_name} to {greeting.to_name}')

@app.timer(interval=1.0)
async def example_sender(app):
    await hello.send(
        value=Greeting(from_name='Faust', to_name='you'),
    )

if __name__ == '__main__':
    app.main()
