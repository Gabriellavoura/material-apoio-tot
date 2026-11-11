import uuid
from functools import lru_cache

import boto3

from pipeline.config import get_settings


def _client(servico: str):
    settings = get_settings()
    return boto3.client(
        servico,
        endpoint_url=settings.aws_endpoint_url,
        region_name=settings.aws_region,
        aws_access_key_id=settings.aws_access_key_id,
        aws_secret_access_key=settings.aws_secret_access_key,
    )


@lru_cache
def _url_da_fila(nome: str) -> str:
    return _client("sqs").get_queue_url(QueueName=nome)["QueueUrl"]


def salvar_objeto(bucket: str, chave: str, conteudo: bytes) -> None:
    _client("s3").put_object(
        Bucket=bucket, Key=chave, Body=conteudo, ContentType="image/png"
    )


def ler_objeto(bucket: str, chave: str) -> bytes:
    return _client("s3").get_object(Bucket=bucket, Key=chave)["Body"].read()


def enviar_mensagem(fila: str, corpo: str, grupo: str = "imagens") -> None:
    _client("sqs").send_message(
        QueueUrl=_url_da_fila(fila),
        MessageBody=corpo,
        MessageGroupId=grupo,
        MessageDeduplicationId=str(uuid.uuid4()),
    )


def receber_mensagens(fila: str, espera: int = 20) -> list[dict]:
    resposta = _client("sqs").receive_message(
        QueueUrl=_url_da_fila(fila),
        MaxNumberOfMessages=1,
        WaitTimeSeconds=espera,
    )
    return resposta.get("Messages", [])


def apagar_mensagem(fila: str, recibo: str) -> None:
    _client("sqs").delete_message(QueueUrl=_url_da_fila(fila), ReceiptHandle=recibo)
