from   decouple import config
from   .        import data_validation
import boto3
import json
import uuid
import logging

def aws_client(service):
    """ Function to create a boto3 client
        of an AWS service.
    """

    return boto3.client(
        service_name=service,
        endpoint_url=config('AWS_HOST'),
        region_name=config('AWS_DEFAULT_REGION'),
        aws_access_key_id=config('AWS_KEY'), 
        aws_secret_access_key=config('AWS_SECRET')
    )

def pool_message(sqs_client):
    """ Function to pool a message from the SQS QUEUE
        and delete the message after poolling it.
    """

    try:
        # Receive message from SQS queue
        response = sqs_client.receive_message(
            QueueUrl=config('SQS_URL'),
            AttributeNames=[
                'SentTimestamp'
            ],
            MaxNumberOfMessages=1,
            MessageAttributeNames=[
                'All'
            ],
            VisibilityTimeout=0,
            WaitTimeSeconds=5
        )

        # Checking if there is a message in the response
        if 'Messages' in response:
            # Getting the message from the api response
            message        = response['Messages'][0]['Body']
            receipt_handle = response['Messages'][0]['ReceiptHandle']
            
            # Delete received message from queue
            sqs_client.delete_message(
                QueueUrl=config('SQS_URL'),
                ReceiptHandle=receipt_handle
            )

            # Data validation
            object = data_validation.validate_pooling_data(message)

            return object
        else:
            return False
    except:
        logging.warning('AWS connection failed...')
        return False
    
def save_message(s3_client, message):
    """ Function to save a message that has 
        been validated into a bucket.  
    """

    try:
        logging.warning('Putting message into the bucket...')

        # Setting params for s3
        bucket_name  = str(message['genre']).lower()
        object_key   = str(message['title']) + '.json'
        file_content = json.dumps(message)

        # Saving object
        s3_client.put_object(
            Bucket=bucket_name, 
            Key=object_key, 
            Body=file_content
        )

        logging.warning('Object <{}> saved'.format(object_key))

        return True
    except:
        # Logging error before returning false
        logging.warning('AWS connection failed...')
        logging.warning('Object NOT saved')
        return False

def input_sqs(data):
    """ Function to send a message to an AWS SQS
        QUEUE.
    """
    
    # Create SQS client
    sqs = aws_client('sqs')

    queue_url = config('SQS_URL')
    unique_id = uuid.uuid4()
    unique_id_str = str(unique_id)

    # Send message to SQS queue
    response = sqs.send_message(
        QueueUrl=queue_url,
        MessageDeduplicationId=unique_id_str,
        MessageGroupId='test',
        MessageBody=data
    )

    logging.warning(response['MessageId'])


    return True