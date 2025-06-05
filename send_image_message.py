import boto3

# Configuração comum
common_args = {
    "aws_access_key_id": "test",
    "aws_secret_access_key": "test",
    "region_name": "us-east-1",
    "endpoint_url": "http://localhost:4566"
}

# Nome da imagem e buckets/filas
filename = "teste.png"
BUCKET_NAME = "image-input"
QUEUE_URL = "http://localhost:4566/000000000000/new-image-input.fifo"

# Inicializa clientes S3 e SQS
s3 = boto3.client("s3", **common_args)
sqs = boto3.client("sqs", **common_args)

# Envia imagem para o S3
with open(filename, "rb") as f:
    s3.upload_fileobj(f, BUCKET_NAME, filename)
    print(f"✅ Imagem enviada para o bucket: {BUCKET_NAME}/{filename}")

# Envia mensagem para a fila SQS
response = sqs.send_message(
    QueueUrl=QUEUE_URL,
    MessageBody=filename,
    MessageGroupId="image-processing"
)
print(f"📨 Mensagem enviada para a fila: {filename}")
print("🆔 MessageId:", response["MessageId"])
