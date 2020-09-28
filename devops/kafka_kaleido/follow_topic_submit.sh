#!/usr/bin/env sh
# Command line tool to interact with Kafka on Kaleido
# Examples: https://github.com/edenhill/kafkacat#examples

source ../../.env && \
docker run -it --network=host edenhill/kafkacat:1.6.0 \
  -b $KALEIDO_BROKER_URLS -L  \
  -X security.protocol=SASL_SSL \
  -X sasl.mechanism=PLAIN \
  -X sasl.username=$KALEIDO_BROKER_KEY \
  -X sasl.password=$KALEIDO_BROKER_SECRET \
  -o -5 \
  -D \\n\\n \
  -J \
  -C -t $KALEIDO_SUBMIT_TOPIC
