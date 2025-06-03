import boto3
import time
from botocore.exceptions import ClientError
import os

def get_aws_clients():
    endpoint_url = os.getenv('AWS_ENDPOINT_URL', 'http://localhost:4566')
   
    s3_client = boto3.client(
        's3',
        endpoint_url=endpoint_url,
        aws_access_key_id='test',
        aws_secret_access_key='test',
        region_name='us-east-1'
    )
   
    sqs_client = boto3.client(
        'sqs',
        endpoint_url=endpoint_url,
        aws_access_key_id='test',
        aws_secret_access_key='test',
        region_name='us-east-1'
    )
   
    return s3_client, sqs_client

def create_s3_buckets(s3_client):
    buckets = ['image-input', 'image-processed']
   
    for bucket_name in buckets:
        try:
            s3_client.create_bucket(Bucket=bucket_name)
            print(f"Created S3 bucket: {bucket_name}")
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyExists':
                print(f"S3 bucket already exists: {bucket_name}")
            else:
                print(f"Error creating bucket {bucket_name}: {e}")

def create_sqs_queues(sqs_client):
    queues = [
        {
            'name': 'new-image-input.fifo',
            'attributes': {
                'FifoQueue': 'true',
                'ContentBasedDeduplication': 'true',
                'MessageRetentionPeriod': '1209600'
            }
        },
        {
            'name': 'new-image-processed.fifo',
            'attributes': {
                'FifoQueue': 'true',
                'ContentBasedDeduplication': 'true',
                'MessageRetentionPeriod': '1209600'
            }
        }
    ]
   
    for queue_config in queues:
        try:
            response = sqs_client.create_queue(
                QueueName=queue_config['name'],
                Attributes=queue_config['attributes']
            )
            print(f"Created SQS queue: {queue_config['name']}")
            print(f"  Queue URL: {response['QueueUrl']}")
        except ClientError as e:
            if e.response['Error']['Code'] == 'QueueAlreadyExists':
                print(f"SQS queue already exists: {queue_config['name']}")
            else:
                print(f"Error creating queue {queue_config['name']}: {e}")

def wait_for_localstack():
    max_retries = 30
    retry_count = 0
   
    while retry_count < max_retries:
        try:
            s3_client, sqs_client = get_aws_clients()
            s3_client.list_buckets()
            sqs_client.list_queues()
            print("LocalStack is ready!")
            return True
        except Exception as e:
            print(f"Waiting for LocalStack... ({retry_count + 1}/{max_retries})")
            time.sleep(2)
            retry_count += 1
   
    print("Failed to connect to LocalStack after maximum retries")
    return False

def main():
    print("Initializing AWS resources...")
   
    if not wait_for_localstack():
        exit(1)
   
    try:
        s3_client, sqs_client = get_aws_clients()
       
        print("\nCreating S3 buckets...")
        create_s3_buckets(s3_client)
       
        print("\nCreating SQS queues...")
        create_sqs_queues(sqs_client)
       
        print("\nAWS resources initialized successfully!")
       
    except Exception as e:
        print(f"Error initializing AWS resources: {e}")
        exit(1)

if __name__ == "__main__":
    main()