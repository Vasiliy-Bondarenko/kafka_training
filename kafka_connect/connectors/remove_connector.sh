#!/usr/bin/env bash

# run this command to remove connector
# be carefull with this command in production :)
# > ./remove_connector <CONNECTOR_NAME>

echo
echo Deleting connector
curl -X DELETE http://localhost:8083/connectors/$1
