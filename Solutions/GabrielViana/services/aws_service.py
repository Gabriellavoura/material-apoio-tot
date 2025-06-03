"""
AWS Service Layer
Handles all interactions with AWS services (S3 and SQS) via LocalStack
"""

import boto3
import json
import os
from botocore.exceptions import ClientError, NoCredentialsError
import logging

logger = logging.getLogger(__name__)

class AWSService:
    def __init__(self):
        """Initialize AWS service clients"""
        self.endpoint_url = os.getenv('AWS_ENDPOINT_URL', 'http://localhost:4566')
        self.region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        
        try:
            # Initialize S3 client
            self.s3_client = boto3.client(
                's3',
                endpoint_url=self.endpoint_url,
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', 'test'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'test'),
                region_name=self.region
            )
            
            # Initialize SQS client
            self.sqs_client = boto3.client(
                'sqs',
                endpoint_url=self.endpoint_url,
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', 'test'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'test'),
                region_name=self.region
            )
            
            # Cache for SQS queue URLs
            self._queue_url_cache = {}
            
        except Exception as e:
            logger.error(f"Failed to initialize AWS clients: {str(e)}")
            raise
    
    def upload_to_s3(self, bucket_name, key, file_content, content_type='application/octet-stream'):
        """
        Upload file content to S3 bucket
        
        Args:
            bucket_name (str): Name of the S3 bucket
            key (str): Object key (filename)
            file_content (bytes): File content to upload
            content_type (str): MIME type of the file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.s3_client.put_object(
                Bucket=bucket_name,
                Key=key,
                Body=file_content,
                ContentType=content_type
            )
            logger.info(f"Successfully uploaded {key} to bucket {bucket_name}")
            return True
            
        except ClientError as e:
            logger.error(f"Failed to upload {key} to bucket {bucket_name}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error uploading to S3: {str(e)}")
            return False
    
    def download_from_s3(self, bucket_name, key):
        """
        Download file content from S3 bucket
        
        Args:
            bucket_name (str): Name of the S3 bucket
            key (str): Object key (filename)
            
        Returns:
            bytes: File content if successful, None otherwise
        """
        try:
            response = self.s3_client.get_object(Bucket=bucket_name, Key=key)
            content = response['Body'].read()
            logger.info(f"Successfully downloaded {key} from bucket {bucket_name}")
            return content
            
        except ClientError as e:
            error_code = e.response['Error']['Code']
            if error_code == 'NoSuchKey':
                logger.error(f"File {key} not found in bucket {bucket_name}")
            else:
                logger.error(f"Failed to download {key} from bucket {bucket_name}: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error downloading from S3: {str(e)}")
            return None
    
    def _get_queue_url(self, queue_name):
        """
        Get SQS queue URL (with caching)
        
        Args:
            queue_name (str): Name of the SQS queue
            
        Returns:
            str: Queue URL if found, None otherwise
        """
        if queue_name in self._queue_url_cache:
            return self._queue_url_cache[queue_name]
        
        try:
            response = self.sqs_client.get_queue_url(QueueName=queue_name)
            queue_url = response['QueueUrl']
            self._queue_url_cache[queue_name] = queue_url
            return queue_url
            
        except ClientError as e:
            logger.error(f"Failed to get queue URL for {queue_name}: {str(e)}")
            return None
    
    def send_sqs_message(self, queue_name, message_body, message_group_id=None, message_deduplication_id=None):
        """
        Send message to SQS queue
        
        Args:
            queue_name (str): Name of the SQS queue
            message_body (str): Message content
            message_group_id (str): Message group ID for FIFO queues
            message_deduplication_id (str): Deduplication ID for FIFO queues
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            queue_url = self._get_queue_url(queue_name)
            if not queue_url:
                return False
            
            message_params = {
                'QueueUrl': queue_url,
                'MessageBody': message_body
            }
            
            # Add FIFO-specific parameters if provided
            if message_group_id:
                message_params['MessageGroupId'] = message_group_id
            if message_deduplication_id:
                message_params['MessageDeduplicationId'] = message_deduplication_id
            
            response = self.sqs_client.send_message(**message_params)
            logger.info(f"Successfully sent message to queue {queue_name}")
            return True
            
        except ClientError as e:
            logger.error(f"Failed to send message to queue {queue_name}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error sending SQS message: {str(e)}")
            return False
    
    def receive_sqs_messages(self, queue_name, max_messages=1, wait_time_seconds=1):
        """
        Receive messages from SQS queue
        
        Args:
            queue_name (str): Name of the SQS queue
            max_messages (int): Maximum number of messages to receive
            wait_time_seconds (int): Long polling wait time
            
        Returns:
            list: List of messages, empty list if none available
        """
        try:
            queue_url = self._get_queue_url(queue_name)
            if not queue_url:
                return []
            
            response = self.sqs_client.receive_message(
                QueueUrl=queue_url,
                MaxNumberOfMessages=max_messages,
                WaitTimeSeconds=wait_time_seconds,
                MessageAttributeNames=['All']
            )
            
            messages = response.get('Messages', [])
            if messages:
                logger.info(f"Received {len(messages)} message(s) from queue {queue_name}")
            
            return messages
            
        except ClientError as e:
            logger.error(f"Failed to receive messages from queue {queue_name}: {str(e)}")
            return []
        except Exception as e:
            logger.error(f"Unexpected error receiving SQS messages: {str(e)}")
            return []
    
    def delete_sqs_message(self, queue_name, receipt_handle):
        """
        Delete message from SQS queue
        
        Args:
            queue_name (str): Name of the SQS queue
            receipt_handle (str): Receipt handle of the message to delete
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            queue_url = self._get_queue_url(queue_name)
            if not queue_url:
                return False
            
            self.sqs_client.delete_message(
                QueueUrl=queue_url,
                ReceiptHandle=receipt_handle
            )
            logger.info(f"Successfully deleted message from queue {queue_name}")
            return True
            
        except ClientError as e:
            logger.error(f"Failed to delete message from queue {queue_name}: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error deleting SQS message: {str(e)}")
            return False
    
    def check_s3_health(self):
        """
        Check S3 service health
        
        Returns:
            bool: True if S3 is accessible, False otherwise
        """
        try:
            self.s3_client.list_buckets()
            return True
        except Exception as e:
            logger.error(f"S3 health check failed: {str(e)}")
            return False
    
    def check_sqs_health(self):
        """
        Check SQS service health
        
        Returns:
            bool: True if SQS is accessible, False otherwise
        """
        try:
            self.sqs_client.list_queues()
            return True
        except Exception as e:
            logger.error(f"SQS health check failed: {str(e)}")
            return False