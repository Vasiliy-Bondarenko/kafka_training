FROM python:3.7
RUN echo "Installing Confluent Cloud client"
RUN curl -L --http1.1 https://cnfl.io/ccloud-cli | sh -s -- -b /usr/local/bin
RUN mkdir /app
WORKDIR /app
