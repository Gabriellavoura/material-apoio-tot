import boto3
import json
import os

# Credenciais falsas para uso com LocalStack
os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"

ENDPOINT_URL = "http://localhost:4566"
SQS_INPUT_QUEUE = "new-image-input.fifo"
SQS_PROCESSED_QUEUE = "new-image-processed.fifo"

sqs_client = boto3.client('sqs', endpoint_url=ENDPOINT_URL, region_name='us-east-1')

def get_queue_url(queue_name):
    response = sqs_client.get_queue_url(QueueName=queue_name)
    return response['QueueUrl']

def send_message(queue_name, message_body, message_group_id='image_processing', message_deduplication_id=None):
    queue_url = get_queue_url(queue_name)
    params = {
        'QueueUrl': queue_url,
        'MessageBody': json.dumps(message_body),
        'MessageGroupId': message_group_id,
    }
    if message_deduplication_id:
        params['MessageDeduplicationId'] = message_deduplication_id
    return sqs_client.send_message(**params)

def receive_messages(queue_name, max_messages=1, wait_time=20):
    queue_url = get_queue_url(queue_name)
    response = sqs_client.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=max_messages,
        WaitTimeSeconds=wait_time,
    )
    return response.get('Messages', [])

def delete_message(queue_name, receipt_handle):
    queue_url = get_queue_url(queue_name)
    sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
