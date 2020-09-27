#!/usr/bin/env bash
docker-compose up -d devops
./ccloud.sh kafka topic create logs --partitions 12
