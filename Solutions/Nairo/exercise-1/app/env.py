import os

#ENDPOINT_URL = 'http://192.168.42.33:4566'
ENDPOINT_URL = os.getenv('ENDPOINT_URL', 'http://host.docker.internal:4566')
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'test')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY', 'test')
REGION_NAME = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')

INPUT_QUEUE_URL = os.getenv('INPUT_QUEUE_URL', 'http://localhost:4566/000000000000/InputQueue.fifo')
OUTPUT_QUEUE_URL = os.getenv('OUTPUT_QUEUE_URL', 'http://localhost:4566/000000000000/InputQueue.fifo')