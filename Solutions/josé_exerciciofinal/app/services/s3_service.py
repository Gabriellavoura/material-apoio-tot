import boto3
import os

session = boto3.session.Session()

s3 = session.client(
    service_name="s3",
    endpoint_url='http://localstack:4566',
    region_name='us-east-1',
    aws_access_key_id='test',
    aws_secret_access_key='test'
)

def upload_file(bucket, file_name, file_data):
    s3.upload_fileobj(file_data, bucket, file_name)

def download_file(bucket, file_name):
    obj = s3.get_object(Bucket=bucket, Key=file_name)
    return obj['Body'].read()
