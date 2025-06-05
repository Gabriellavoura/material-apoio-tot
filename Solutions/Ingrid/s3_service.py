import boto3
import os

# Credenciais falsas para uso com LocalStack
os.environ["AWS_ACCESS_KEY_ID"] = "test"
os.environ["AWS_SECRET_ACCESS_KEY"] = "test"

ENDPOINT_URL = "http://localhost:4566"

s3_client = boto3.client('s3', endpoint_url=ENDPOINT_URL, region_name='us-east-1')

def download_file(bucket_name, object_key):
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    return response['Body'].read()

def upload_fileobj(file_obj, bucket_name, object_key):
    s3_client.upload_fileobj(file_obj, bucket_name, object_key)
