import boto3
import botocore
import cv2
import numpy as np

AWS_REGION = "us-east-1"
common_args = {
    "aws_access_key_id": "test",
    "aws_secret_access_key": "test",
    "region_name": AWS_REGION,
    "endpoint_url": "http://localhost:4566"
}

s3 = boto3.client("s3", **common_args)
sqs = boto3.client("sqs", **common_args)


def ensure_bucket_exists(bucket_name):
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"✅ Bucket encontrado: {bucket_name}")
    except botocore.exceptions.ClientError:
        print(f"📂 Bucket {bucket_name} não existe. Criando...")
        s3.create_bucket(Bucket=bucket_name)
        print(f"✅ Bucket criado: {bucket_name}")


def ensure_queue_exists(queue_url):
    try:
        print(f"⏳ Verificando existência da fila: {queue_url}")
        sqs.get_queue_attributes(QueueUrl=queue_url, AttributeNames=["All"])
        print(f"✅ Fila encontrada e pronta.")
    except botocore.exceptions.ClientError as e:
        print(f"❌ Erro ao verificar a fila: {e}")
        exit(1)


def process_image(image_bytes: bytes) -> bytes:
    np_array = np.frombuffer(image_bytes, np.uint8)
    image = cv2.imdecode(np_array, cv2.IMREAD_GRAYSCALE)
    _, processed = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    _, buffer = cv2.imencode(".png", processed)
    return buffer.tobytes()
