#!/usr/bin/env bash
curl -X POST \
  http://localhost:8083/connectors \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{
  "name": "eth_gateway_v.0.1",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "tasks.max": "3",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "io.confluent.connect.avro.AvroConverter",
    "topics": "eth_transactions_submit,eth_transactions_receive",
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
