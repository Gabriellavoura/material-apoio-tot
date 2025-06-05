import boto3
import os
import time

# Configuração para acessar o LocalStack
endpoint_url = "http://localhost:4566"

def create_s3_buckets():
    """Cria os buckets S3 necessários para o pipeline de processamento de imagens."""
    s3 = boto3.client('s3', endpoint_url=endpoint_url)
    
    # Criar buckets
    buckets = ['image-input', 'image-processed']
    for bucket in buckets:
        try:
            s3.create_bucket(Bucket=bucket)
            print(f"Bucket '{bucket}' criado com sucesso.")
        except Exception as e:
            print(f"Erro ao criar bucket '{bucket}': {e}")

def create_sqs_queues():
    """Cria as filas SQS .fifo necessárias para o pipeline de processamento de imagens."""
    sqs = boto3.client('sqs', endpoint_url=endpoint_url)
    
    # Criar filas FIFO
    queues = ['new-image-input.fifo', 'new-image-processed.fifo']
    for queue in queues:
        try:
            sqs.create_queue(
                QueueName=queue,
                Attributes={
                    'FifoQueue': 'true',
                    'ContentBasedDeduplication': 'true'
                }
            )
            print(f"Fila '{queue}' criada com sucesso.")
        except Exception as e:
            print(f"Erro ao criar fila '{queue}': {e}")

if __name__ == "__main__":
    # Aguardar o LocalStack iniciar
    print("Aguardando o LocalStack iniciar...")
    time.sleep(5)
    
    # Criar recursos
    create_s3_buckets()
    create_sqs_queues()
    
    print("Configuração dos recursos AWS concluída.")
