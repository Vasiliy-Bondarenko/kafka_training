#!/usr/bin/env bash
docker-compose up -d devops
#./ccloud.sh kafka topic create logs --partitions 12
#./ccloud.sh kafka topic create eth_transaction_requests --partitions 12
#./ccloud.sh kafka topic create eth_transaction_responses --partitions 12

echo
echo 'If you see errors like "You must be logged in to run this command" above - please follow "Login into Confluent Cloud" procedure described in the README file'
echo
