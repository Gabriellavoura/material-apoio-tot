import boto3
import logging
import os
import uuid
from env import *
from botocore.exceptions import ClientError

def configure_sqs_or_s3_client(client_type:str):
    client = boto3.client(client_type, endpoint_url=ENDPOINT_URL,
                                aws_access_key_id=KEY_ID,
                                aws_secret_access_key=ACCESS_KEY,
                                region_name=REGION)
    return client

def upload_file(s3_client, bucket_name, file_path, object_name):
    if object_name is None:
        object_name = os.path.basename(file_path)

    try:
        response = s3_client.upload_file(file_path, bucket_name, object_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def write_message(sqs_client, queue_url: str, message) -> dict:
    """ Publish a new message to a SQS queue.

    :param sqs_client: SQS Client instance.
    :param queue_url: Queue Url.
    :param message: Message to be published.
    :return: True if succeeded, else False.
    """    
    deduplication_id = uuid.uuid4()
    group_id = uuid.uuid4()
    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=message,
        MessageDeduplicationId=str(deduplication_id),
        MessageGroupId=str(group_id))
    return response

   