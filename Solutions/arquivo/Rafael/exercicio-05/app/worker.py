import json
import logging
import os
import time
from datetime import UTC, datetime

import boto3
from botocore.exceptions import ClientError
from app.exercicio_05 import Livro as LivroDB, engine
from exercicio_05 import engine
from sqlalchemy.exc import SQLAlchemyError
from sqlmodel import Session

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

endpoint_url = os.getenv("AWS_ENDPOINT_URL", "http://floci:4566")
sqs = boto3.client("sqs", endpoint_url=endpoint_url)
s3 = boto3.client("s3", endpoint_url=endpoint_url)

FILA_ENTRADA = "livros-entrada.fifo"
FILA_SAIDA = "livros-saida.fifo"


def obter_url_fila(nome_fila: str) -> str:
    for _ in range(10):
        try:
            resposta = sqs.get_queue_url(QueueName=nome_fila)
            return resposta["QueueUrl"]
        except ClientError:
            logger.warning(f"A aguardar disponibilidade da fila {nome_fila}...")
            time.sleep(2)
        except Exception:
            time.sleep(2)
    raise RuntimeError(f"Não foi possível obter a URL da fila {nome_fila}")


def escolher_bucket(genero: str) -> str:
    genero_limpo = str(genero).strip().lower()
    if genero_limpo == "romance":
        return "romance"
    elif genero_limpo == "ficcao":
        return "ficcao"
    return "outros"


def salvar_livro(livro: dict) -> str:
    bucket = escolher_bucket(livro.get("genero", ""))
    titulo = livro.get("titulo", "sem-titulo").replace(" ", "_")
    nome_arquivo = f"{titulo}.json"

    s3.put_object(
        Bucket=bucket,
        Key=nome_arquivo,
        Body=json.dumps(livro),
        ContentType="application/json",
    )
    return f"s3://{bucket}/{nome_arquivo}"


def atualizar_status_db(livro_id: str, status: str, arquivo_s3: str | None = None):
    try:
        with Session(engine) as session:
            livro = session.get(LivroDB, livro_id)
            if livro:
                livro.status = status
                if arquivo_s3:
                    livro.arquivo = arquivo_s3
                livro.atualizado_em = datetime.now(UTC)
                session.add(livro)
                session.commit()
                logger.info(
                    f"Base de Dados: Livro {livro_id} atualizado para status='{status}'"
                )
    except SQLAlchemyError as e:
        logger.error(f"Erro de base de dados ao atualizar status do livro {livro_id}: {e}")
    except Exception as e:
        logger.error(f"Erro inesperado ao atualizar status do livro {livro_id}: {e}")


def processar(mensagem: dict) -> bool:
    try:
        corpo = json.loads(mensagem["Body"])
    except json.JSONDecodeError:
        logger.error("JSON inválido recebido. ignorar para não travar o worker.")
        return True

    livro_id = corpo.get("id")
    if not livro_id:
        logger.error("Mensagem sem ID. ignorar.")
        return True

    try:
        caminho_s3 = salvar_livro(corpo)
        logger.info(f"Livro {livro_id} guardado em {caminho_s3}")

        atualizar_status_db(livro_id, "processado", caminho_s3)

        mensagem_saida = {"id": livro_id, "arquivo": caminho_s3}
        sqs.send_message(
            QueueUrl=obter_url_fila(FILA_SAIDA),
            MessageBody=json.dumps(mensagem_saida),
            MessageGroupId="processados",
            MessageDeduplicationId=str(livro_id),
        )
        logger.info(f"Aviso enviado para a fila de saída (Livro ID: {livro_id})")
        return True
    except Exception as e:
        logger.error(f"Erro ao processar livro {livro_id}: {e}")
        atualizar_status_db(livro_id, "erro")
        return False


def main():
    logger.info("Worker iniciado")
    url_entrada = obter_url_fila(FILA_ENTRADA)

    while True:
        resposta = sqs.receive_message(
            QueueUrl=url_entrada, MaxNumberOfMessages=1, WaitTimeSeconds=20
        )

        mensagens = resposta.get("Messages", [])
        if not mensagens:
            continue

        for msg in mensagens:
            recibo = msg["ReceiptHandle"]
            sucesso = processar(msg)

            if sucesso:
                sqs.delete_message(QueueUrl=url_entrada, ReceiptHandle=recibo)
                logger.info("Mensagem eliminada da fila de entrada com sucesso.\n")


if __name__ == "__main__":
    main()