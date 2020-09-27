#!/usr/bin/env bash
docker-compose up -d devops
./ccloud.sh kafka topic list
