FROM python:3.7
RUN pip install confluent-kafka requests
RUN pip install confluent_kafka[avro]
RUN pip install faust
RUN pip install Faker
RUN pip install web3
RUN pip install python-schema-registry-client[faust]
WORKDIR /app
