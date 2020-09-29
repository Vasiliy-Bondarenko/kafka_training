#!/usr/bin/env bash

echo CONNECT_BOOTSTRAP_SERVERS = $CONNECT_BOOTSTRAP_SERVERS

#echo "Installing connector plugins"
#confluent-hub install --no-prompt debezium/debezium-connector-mysql:0.10.0
#confluent-hub install --no-prompt debezium/debezium-connector-sqlserver:0.10.0
#confluent-hub install --no-prompt snowflakeinc/snowflake-kafka-connector:0.5.5

echo "Launching Kafka Connect worker"
/etc/confluent/docker/run &

echo "Waiting for Kafka Connect to start listening on localhost:8083 ⏳"
while : ; do
    curl_status=$(curl -s -o /dev/null -w %{http_code} http://localhost:8083/connectors)
    echo -e $(date) " Kafka Connect listener HTTP state: " $curl_status " (waiting for 200)"
    if [ $curl_status -eq 200 ] ; then
    break
    fi
    sleep 5
done

echo "Kafka Connect started!"
echo "Creating logs connector - it can fail if connector already exists - that's fine!"
/app/connectors/logs.sh
/app/connectors/eth_gateway.sh
echo

sleep infinity
