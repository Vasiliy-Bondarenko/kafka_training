#!/usr/bin/env python
#
# Copyright 2020 Confluent Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# =============================================================================
#
# Consume messages from Confluent Cloud
# Using Confluent Python Client for Apache Kafka
#
# =============================================================================

from confluent_kafka import Consumer
import json
import ccloud_lib


if __name__ == '__main__':

    # Initialization
    args = ccloud_lib.parse_args()
    config_file = args.config_file
    topic = "users3"
    conf = ccloud_lib.read_ccloud_config(config_file)

    # Create Consumer instance
    c = Consumer({
        'bootstrap.servers': conf['bootstrap.servers'],
        # 'sasl.mechanisms': conf['sasl.mechanisms'],
        # 'security.protocol': conf['security.protocol'],
        # 'sasl.username': conf['sasl.username'],
        # 'sasl.password': conf['sasl.password'],
        'group.id': 'python_example_group_2',

        # to start reading from the beginning of the topic if no committed offsets exist or current offset is invalid
        # 'earliest' | 'latest' | 'none' - throw an exception if no offset is found (not working in this client for some reason)
        'auto.offset.reset': 'earliest',

        'enable.auto.commit': False,
    })

    # Subscribe to topic
    c.subscribe([topic])

    # Process messages
    try:
        while True:
            msg = c.poll(1.0)
            if msg is None:
                # No message available within timeout.
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                print("Waiting for message or event/error in poll()")
                continue
            elif msg.error():
                print('error: {}'.format(msg.error()))
            else:
                # ------------ your code here ---------------
                # Check for Kafka message
                record_key = msg.key()
                record_value = msg.value()
                # data = json.loads(record_value)
                print(f"{topic}/{msg.partition()}/{msg.offset()}: {record_key}: {record_value}")
                c.commit()
                # ------------ /your code here ---------------

    except KeyboardInterrupt:
        pass
    finally:
        # Leave group and commit final offsets
        c.close()
