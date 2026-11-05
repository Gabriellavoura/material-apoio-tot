import os
import time

import boto3


def criar_cliente_s3():
    return boto3.client("s3", endpoint_url=os.getenv("AWS_ENDPOINT_URL"))


def criar_cliente_sqs():
    return boto3.client("sqs", endpoint_url=os.getenv("AWS_ENDPOINT_URL"))


def buscar_url_da_fila(nome_da_fila: str) -> str:
    for tentativa in range(30):
        try:
            resposta = criar_cliente_sqs().get_queue_url(QueueName=nome_da_fila)
            return resposta["QueueUrl"]
        except Exception:
            if tentativa == 29:
                raise
            time.sleep(1)

    raise RuntimeError(f"Fila não encontrada: {nome_da_fila}")
