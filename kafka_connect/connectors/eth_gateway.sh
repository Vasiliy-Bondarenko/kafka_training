#!/usr/bin/env bash
# connection docs: https://docs.confluent.io/current/schema-registry/connect.html
curl -X POST \
  http://localhost:8083/connectors \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{
  "name": "eth_gateway_v.0.3",
  "config": {
    "consumer.override.auto.offset.reset": "earliest",
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "tasks.max": "1",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "io.confluent.connect.avro.AvroConverter",
    "topics": "eth_transactions_submit,eth_transactions_receive,eth_events",
    "connection.url": "jdbc:postgresql://db:5432/postgres",
    "connection.user": "postgres",
    "connection.password": "open",
    "dialect.name": "PostgreSqlDatabaseDialect",
    "insert.mode": "upsert",
    "batch.size": "1000",
    "pk.mode": "record_value",
    "pk.fields": "id",
    "auto.create": "true",
    "auto.evolve": "true",
    "value.converter.schema.registry.url": "'${SCHEMA_REGISTRY_ENDPOINT}'",
    "value.converter.basic.auth.credentials.source": "USER_INFO",
    "value.converter.basic.auth.user.info": "'${SCHEMA_REGISTRY_KEY}':'${SCHEMA_REGISTRY_SECRET}'",

    "transforms": "InsertMessageTime",
    "transforms.InsertMessageTime.type":"org.apache.kafka.connect.transforms.InsertField$Value",
    "transforms.InsertMessageTime.timestamp.field":"updated_at"
  }
}'
