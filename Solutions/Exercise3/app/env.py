import os

ENDPOINT_URL = os.getenv('ENDPOINT_URL', 'http://host.docker.internal:4566/')
KEY_ID = os.getenv('AWS_ACCESS_KEY_ID', 'test')
ACCESS_KEY = os.getenv('AWS_SECRET_KEY', 'test')
REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')

INPUT_QUEUE_NAME = os.getenv("INPUT_QUEUE_NAME","InputQueue")
INPUT_QUEUE_URL = os.getenv("INPUT_QUEUE_URL", "http://host.docker.internal:4566//000000000000/InputQueue.fifo")
OUTPUT_QUEUE_NAME = os.getenv("OUTPUT_QUEUE_NAME","OutputQueue")
OUTPUT_QUEUE_URL = os.getenv("INPUT_QUEUE_URL", "http://host.docker.internal:4566//000000000000/OutputQueue.fifo")

BUCKET_A = os.getenv("BUCKET_A", 'scifi')
BUCKET_B = os.getenv("BUCKET_B", 'romance')
