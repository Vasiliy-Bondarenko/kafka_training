Kafka Faker
===========

Generates messages to Kafka for testing purposes



Usage
------

If you do not have a cluster running locally you can use `docker-compose` to avoid several headaches.
By default the `KAFKA_BOOTSTRAP_SERVER` is `kafka://localhost:29092`.

```bash
make kafka-cluster
```

Then, start the `Faust application`:

```bash
make start-app
```

Settings
--------

Settings are created based on [local-settings](https://github.com/drgarcia1986/simple-settings) package.

Look for settings in `app/settings.py`.

Basic Commands
--------------

* Install requirements locally: `make install-test`
* Inside docker container:
    * Start Faust application: `make start-app`
    * List topics: `make list-topics`
    * Create topic: `make create-topic={topic-name}`
    * List agents: `make list-agents`
    * Send events to page_view topic/agent: `make send-page-view-event payload='{"id": "foo", "user": "bar"}'`

Run tests
---------

```sh
make install-test && ./scripts/test
```

Lint code
---------

```sh
./scripts/lint
```

Type checks
-----------

Running type checks with mypy:

```sh
mypy kafka_processors
```
