import json

import boto3

from app.fila import enviar_imagem


def test_enviar_imagem_coloca_mensagem_na_fila(aws):
    enviar_imagem("abc", "abc.png")

    sqs = boto3.client("sqs")
    url = sqs.get_queue_url(QueueName="new-image-input.fifo")["QueueUrl"]
    mensagens = sqs.receive_message(QueueUrl=url).get("Messages", [])

    assert len(mensagens) == 1
    assert json.loads(mensagens[0]["Body"]) == {"id": "abc", "chave": "abc.png"}