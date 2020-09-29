#!/usr/bin/env bash
source ../.env
docker-compose up -d devops
./ccloud.sh kafka topic create logs --partitions 12
./ccloud.sh kafka topic create $KALEIDO_SUBMIT_TOPIC --partitions 12
./ccloud.sh kafka topic create $KALEIDO_RECEIVE_TOPIC --partitions 12
./ccloud.sh kafka topic create eth_transactions_submit --partitions 12
./ccloud.sh kafka topic create eth_transactions_receive --partitions 12

echo
echo 'If you see errors like "You must be logged in to run this command" above - please follow "Login into Confluent Cloud" procedure described in the README file'
echo
