import os
import time
import json
import boto3
from botocore.exceptions import ClientError

AWS_ENDPOINT_URL = os.getenv("AWS_ENDPOINT_URL", "http://localhost:4566")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")

sqs = boto3.client("sqs", endpoint_url=AWS_ENDPOINT_URL, region_name=AWS_REGION, aws_access_key_id="test", aws_secret_access_key="test")
s3 = boto3.client("s3", endpoint_url=AWS_ENDPOINT_URL, region_name=AWS_REGION, aws_access_key_id="test", aws_secret_access_key="test")

FILA_ENTRADA = "livros-entrada.fifo"
FILA_SAIDA = "livros-saida.fifo"

def obter_url_fila(nome_fila):
    while True:
        try:
            resposta = sqs.get_queue_url(QueueName=nome_fila)
            return resposta["QueueUrl"]
        except ClientError as e:
            if e.response["Error"]["Code"] == "AWS.SimpleQueueService.NonExistentQueue":
                print(f"[*] Fila '{nome_fila}' ainda não existe. tentando em 2 seg.")
                time.sleep(2)
            else:
                raise

def processar_mensagem(msg, queue_url):
    body_str = msg.get("Body", "{}")
    msg_id = msg.get("MessageId")
    receipt_handle = msg.get("ReceiptHandle")
    
    try:
        livro = json.loads(body_str)
        categoria = livro.get("categoria", livro.get("genero", "outros")).lower()
    except json.JSONDecodeError:
        categoria = "outros"

    if categoria == "romance":
        bucket_destino = "romance"
    elif categoria == "ficcao" or categoria == "ficção":
        bucket_destino = "ficcao"
    else:
        bucket_destino = "outros"

    print(f"+ Mensagem recebida. destino:'{bucket_destino}'")
    
    file_key = f"livro_{msg_id}.json"
    s3.put_object(Bucket=bucket_destino, Key=file_key, Body=body_str)
    
    sqs.delete_message(QueueUrl=queue_url, ReceiptHandle=receipt_handle)
    print("- Mensagem fila.")

def main():
    print("* Worker iniciado. Aguardando")
    url_entrada = obter_url_fila(FILA_ENTRADA)
    print(f"* À escuta na fila: {url_entrada}")
    
    while True:
        resposta = sqs.receive_message(
            QueueUrl=url_entrada,
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20
        )
        
        mensagens = resposta.get("Messages", [])
        for msg in mensagens:
            processar_mensagem(msg, url_entrada)

if __name__ == "__main__":
    main()