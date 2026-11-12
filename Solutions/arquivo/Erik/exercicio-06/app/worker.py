import json
import logging

import boto3
from sqlmodel import Session, create_engine

from app.config import DATABASE_URL
from app.models import ImagemDB, agora
from app.processamento import binarizar

FILA_ENTRADA = "new-image-input.fifo"
FILA_SAIDA = "new-image-processed.fifo"
BUCKET_ENTRADA = "image-input"
BUCKET_SAIDA = "image-output"

logger = logging.getLogger("worker")


def atualizar_status(
    session: Session, imagem_id: str, status: str, erro: str | None = None
) -> None:
    """Atualiza o status da imagem no banco."""
    imagem = session.get(ImagemDB, imagem_id)
    if imagem is None:
        logger.warning("Imagem %s não está no banco", imagem_id)
        return
    imagem.status = status
    imagem.erro = erro
    if status == "processada":
        imagem.concluido_em = agora()
    session.add(imagem)
    session.commit()


def processar(mensagem: dict, s3, sqs, url_saida: str, session: Session) -> None:
    """Baixa, binariza, guarda o resultado, atualiza o banco e avisa a fila."""
    corpo = json.loads(mensagem["Body"])
    imagem_id = corpo["id"]
    chave = corpo["chave"]
    try:
        original = s3.get_object(Bucket=BUCKET_ENTRADA, Key=chave)["Body"].read()
        resultado = binarizar(original)
        s3.put_object(
            Bucket=BUCKET_SAIDA,
            Key=chave,
            Body=resultado,
            ContentType="image/png",
        )
        atualizar_status(session, imagem_id, "processada")
        sqs.send_message(
            QueueUrl=url_saida,
            MessageBody=json.dumps(
                {"id": imagem_id, "arquivo": f"s3://{BUCKET_SAIDA}/{chave}"}
            ),
            MessageGroupId="imagens",
            MessageDeduplicationId=imagem_id,
        )
    except Exception as exc:
        session.rollback()
        atualizar_status(session, imagem_id, "erro", str(exc))
        raise
    logger.info("Imagem %s processada: s3://%s/%s", imagem_id, BUCKET_SAIDA, chave)


def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    engine = create_engine(DATABASE_URL)
    s3 = boto3.client("s3")
    sqs = boto3.client("sqs")
    url_entrada = sqs.get_queue_url(QueueName=FILA_ENTRADA)["QueueUrl"]
    url_saida = sqs.get_queue_url(QueueName=FILA_SAIDA)["QueueUrl"]
    logger.info("Worker iniciado, esperando mensagens")

    while True:
        resposta = sqs.receive_message(
            QueueUrl=url_entrada, MaxNumberOfMessages=10, WaitTimeSeconds=20
        )
        for mensagem in resposta.get("Messages", []):
            try:
                with Session(engine) as session:
                    processar(mensagem, s3, sqs, url_saida, session)
            except (json.JSONDecodeError, KeyError):
                logger.error("Mensagem inválida, descartando: %s", mensagem["Body"])
            except ValueError:
                logger.error("Imagem inválida, status 'erro' registrado, descartando")
            except Exception:
                logger.exception("Erro ao processar, a mensagem volta para a fila")
                continue
            sqs.delete_message(
                QueueUrl=url_entrada, ReceiptHandle=mensagem["ReceiptHandle"]
            )


if __name__ == "__main__":
    main()