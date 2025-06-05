from botocore.exceptions import ClientError
import boto3
import os
import uuid


class SQSService:
    def __init__(self):
        self.sqs = boto3.client(
            'sqs',
            endpoint_url=os.getenv('SQS_ENDPOINT', 'http://localstack:4566'),
            region_name=os.getenv('AWS_REGION', 'us-east-1'),
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID', 'test'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY', 'test')
        )


        # Cria filas se não existirem
        self.queue_url_input = self.create_queue_if_not_exists('new-image-input.fifo')
        self.queue_url_processed = self.create_queue_if_not_exists('new-image-processed.fifo')

    def create_queue_if_not_exists(self, queue_name):
        try:
            response = self.sqs.get_queue_url(QueueName=queue_name)
            print(f"Fila {queue_name} já existe.")
            return response['QueueUrl']
        except ClientError as e:
            if e.response['Error']['Code'] == 'AWS.SimpleQueueService.NonExistentQueue':
                print(f"Fila {queue_name} não encontrada. Criando...")
                attributes = {
                    'FifoQueue': 'true',
                    'ContentBasedDeduplication': 'true'
                }
                response = self.sqs.create_queue(
                    QueueName=queue_name,
                    Attributes=attributes
                )
                return response['QueueUrl']
            else:
                raise e

    def send_message(self, queue_url, body, group_id='default'):
        if not queue_url:
            raise ValueError("QueueUrl inválida (None). Verifique se a fila existe.")
        self.sqs.send_message(
            QueueUrl=queue_url,
            MessageBody=body,
            MessageGroupId=group_id,
            MessageDeduplicationId=str(uuid.uuid4())  # necessário para FIFO
        )

    def receive_messages(self, queue_url):
        if not queue_url:
            raise ValueError("QueueUrl inválida (None). Verifique se a fila existe.")
        response = self.sqs.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=2
        )
        return response.get('Messages', [])

    def delete_message(self, queue_url, receipt_handle):
        if not queue_url:
            raise ValueError("QueueUrl inválida (None). Verifique se a fila existe.")
        self.sqs.delete_message(
            QueueUrl=queue_url,
            ReceiptHandle=receipt_handle
        )
