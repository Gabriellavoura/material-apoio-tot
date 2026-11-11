import uuid

import boto3
import pytest
from moto import mock_aws

from pipeline import aws


@pytest.fixture
def fila(monkeypatch):
    with mock_aws():
        monkeypatch.setattr(
            aws,
            "_client",
            lambda servico: boto3.client(servico, region_name="us-east-1"),
        )
        aws._url_da_fila.cache_clear()
        nome = f"teste-{uuid.uuid4().hex[:8]}.fifo"
        boto3.client("sqs", region_name="us-east-1").create_queue(
            QueueName=nome, Attributes={"FifoQueue": "true"}
        )
        yield nome
        aws._url_da_fila.cache_clear()


def test_envio_e_leitura(fila):
    aws.enviar_mensagem(fila, "ola")
    mensagens = aws.receber_mensagens(fila, espera=0)
    assert mensagens[0]["Body"] == "ola"


def test_apagar_mensagem(fila):
    aws.enviar_mensagem(fila, "ola")
    mensagem = aws.receber_mensagens(fila, espera=0)[0]
    aws.apagar_mensagem(fila, mensagem["ReceiptHandle"])
    sqs = boto3.client("sqs", region_name="us-east-1")
    atributos = sqs.get_queue_attributes(
        QueueUrl=aws._url_da_fila(fila), AttributeNames=["All"]
    )["Attributes"]
    assert atributos["ApproximateNumberOfMessages"] == "0"
    assert atributos["ApproximateNumberOfMessagesNotVisible"] == "0"
