import boto3
import uuid
from app.env import *

def instantiate_aws_client(service):
    client = boto3.client(service, endpoint_url=ENDPOINT_URL,
                                aws_access_key_id=AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                                region_name=REGION_NAME)
    return client

def list_queues(sqs_client) -> list:
    try:
        response = sqs_client.list_queues()

        list_of_queues = []
        for queue in response['QueueUrls']:
            list_of_queues.append(queue)
        return list_of_queues

    except Exception as err:
        return err


def read_message(sqs_client, queue_url: str) -> dict:
    try:
        response = sqs_client.receive_message(QueueUrl=queue_url)
        return response

    except Exception as err:
        return err

def write_message(sqs_client, queue_url: str, message) -> dict:
    try:
        deduplication_id = uuid.uuid4()
        group_id = uuid.uuid4()
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message,
            MessageDeduplicationId=str(deduplication_id),
            MessageGroupId=str(group_id))
        return response

    except Exception as err:
        return err


def delete_message(sqs_client, queue_url: str, receipt_handle: str) -> bool:
    try:
        response = sqs_client.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
        return response

    except Exception as err:
        return err
    

def list_buckets_names(s3_client) -> list:
    try:
        response = s3_client.list_buckets()

        bucket_names = []
        for bucket in response['Buckets']:
            bucket_names.append(bucket['Name'])
        return bucket_names

    except Exception as err:
        return err

def list_buckets_content_keys(s3_client, bucket_name) -> list:
    try:
        response = s3_client.list_objects_v2(Bucket=bucket_name)

        if response['KeyCount'] == 0:
            return []
        
        keys = []
        for item in response['Contents']:
            keys.append(item['Key'])
        return keys
    
    except Exception as err:
        return err
    
def upload_file(s3_client, bucket:str, key:str, body:str) -> bool:
    try:
        response = s3_client.put_object(Bucket=bucket, Key=key, Body=body)
        return response
    
    except Exception as err:
        return err
