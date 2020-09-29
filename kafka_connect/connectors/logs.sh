#!/usr/bin/env bash
curl -X POST \
  http://localhost:8083/connectors \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json' \
  -d '{
  "name": "logs",
  "config": {
    "connector.class": "io.confluent.connect.jdbc.JdbcSinkConnector",
    "tasks.max": "3",
    "key.converter": "org.apache.kafka.connect.storage.StringConverter",
    "value.converter": "io.confluent.connect.avro.AvroConverter",
    "topics": "logs",
    "connection.url": "jdbc:postgresql://db:5432/postgres",
    "connection.user": "postgres",
    "connection.password": "open",
    "dialect.name": "PostgreSqlDatabaseDialect",
    "insert.mode": "insert",
    "batch.size": "1000",
    "pk.mode": "kafka",
    "auto.create": "true",
    "auto.evolve": "true",
    "value.converter.schema.registry.url": "'${SCHEMA_REGISTRY_ENDPOINT}'",
    "value.converter.basic.auth.credentials.source": "USER_INFO",
    "value.converter.basic.auth.user.info": "'${SCHEMA_REGISTRY_KEY}':'${SCHEMA_REGISTRY_SECRET}'"
  }
}'
