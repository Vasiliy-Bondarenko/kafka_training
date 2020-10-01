#!/usr/bin/env bash
source .env
#echo ETH_GATEWAY_EVENTS_ENDPOINT_AUTH_KEY=$ETH_GATEWAY_EVENTS_ENDPOINT_AUTH_KEY
docker-compose up -d $1
