#!/bin/bash

# Wait for LocalStack to be ready
echo "Waiting for LocalStack to be ready..."
# while ! nc -z localstack 4566; do
#   sleep 1
# done

echo "LocalStack is ready!"

# Initialize AWS resources
echo "Initializing AWS resources..."
python scripts/init_aws.py

# Start the Flask application
echo "Starting Flask application..."
python app.py