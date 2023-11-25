#!/bin/bash

echo "Starting Docker container..."
docker run --rm -d --name openinterpreterui-test -p 8501:8501 openinterpreterui

echo "Waiting for Healthcheck..."
sleep 10 # Ensure sufficient time for Healthcheck to complete

response=$(curl --silent --fail http://localhost:8501/_stcore/health)

if [ "$response" = "ok" ]; then
    echo "Healthcheck passed. Response body is 'ok'."
    docker stop openinterpreterui-test
    exit 0
else
    echo "Healthcheck failed. Response body: $response"
    docker stop openinterpreterui-test
    exit 1
fi
