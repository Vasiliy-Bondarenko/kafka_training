#!/usr/bin/env bash
source .env
export SCHEMA_REGISTRY_ENDPOINT
export SCHEMA_REGISTRY_KEY
export SCHEMA_REGISTRY_SECRET
cat connector_PGS_config.yaml | envsubst
