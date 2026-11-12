import json

import boto3
import cv2
import numpy as np
import pytest

from app.models import ImagemDB
from app.worker import atualizar_status, processar


def _png() -> bytes:
    imagem = np.tile(np.arange(256, dtype=np.uint8), (64, 1))
    _, buffer = cv2.imencode(".png", imagem)
    return buffer.tobytes()


def _mensagem(imagem_id: str, chave: str) -> dict:
    return {"Body": json.dumps({"id": imagem_id, "chave": chave})}


def _cadastrar(session, imagem_id: str) -> None:
    session.add(ImagemDB(id=imagem_id, nome_original="foto.png"))
    session.commit()


def test_atualizar_status_processada_preenche_conclusao(session):
    _cadastrar(session, "1")

    atualizar_status(session, "1", "processada")

    imagem = session.get(ImagemDB, "1")
    assert imagem.status == "processada"
    assert imagem.concluido_em is not None


def test_atualizar_status_erro_guarda_a_mensagem(session):
    _cadastrar(session, "1")

    atualizar_status(session, "1", "erro", "falhou")

    imagem = session.get(ImagemDB, "1")
    assert imagem.status == "erro"
    assert imagem.erro == "falhou"
    assert imagem.concluido_em is None


def test_atualizar_status_de_imagem_inexistente_nao_quebra(session):
    atualizar_status(session, "nao-existe", "processada")


def test_processar_imagem_valida(aws, session):
    s3 = boto3.client("s3")
    sqs = boto3.client("sqs")
    s3.put_object(Bucket="image-input", Key="1.png", Body=_png())
    _cadastrar(session, "1")
    url_saida = sqs.get_queue_url(QueueName="new-image-processed.fifo")["QueueUrl"]

    processar(_mensagem("1", "1.png"), s3, sqs, url_saida, session)

    assert session.get(ImagemDB, "1").status == "processada"
    s3.head_object(Bucket="image-output", Key="1.png")
    mensagens = sqs.receive_message(QueueUrl=url_saida).get("Messages", [])
    assert json.loads(mensagens[0]["Body"]) == {
        "id": "1",
        "arquivo": "s3://image-output/1.png",
    }


def test_processar_conteudo_invalido_marca_erro(aws, session):
    s3 = boto3.client("s3")
    sqs = boto3.client("sqs")
    s3.put_object(Bucket="image-input", Key="2.png", Body=b"isso nao e uma imagem")
    _cadastrar(session, "2")
    url_saida = sqs.get_queue_url(QueueName="new-image-processed.fifo")["QueueUrl"]

    with pytest.raises(ValueError):
        processar(_mensagem("2", "2.png"), s3, sqs, url_saida, session)

    imagem = session.get(ImagemDB, "2")
    assert imagem.status == "erro"
    assert "imagem válida" in imagem.erro