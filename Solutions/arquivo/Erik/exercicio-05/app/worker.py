import json
import logging

import boto3
from sqlmodel import Session, create_engine

from app.config import DATABASE_URL
from app.models import LivroDB

NOME_FILA_ENTRADA = "livros-entrada.fifo"
NOME_FILA_SAIDA = "livros-saida.fifo"
BUCKETS_CONHECIDOS = {"romance", "ficcao"}

logger = logging.getLogger("worker")

def escolher_bucket(genero: str) -> str:
    """Devolve o bucket do gênero, ou 'outros' se não for um dos conhecidos."""
    if genero in BUCKETS_CONHECIDOS:
        return genero
    return "outros"


def nome_arquivo(livro: dict) -> str:
    """Monta o nome do arquivo: <titulo>.json."""
    return f"{livro['titulo']}.json"


def salvar_livro(livro: dict, s3) -> str:
    """Salva o livro no bucket do gênero e devolve o endereço s3://."""
    bucket = escolher_bucket(livro["genero"])
    chave = nome_arquivo(livro)
    s3.put_object(
        Bucket=bucket,
        Key=chave,
        Body=json.dumps(livro, ensure_ascii=False).encode("utf-8"),
        ContentType="application/json",
    )
    return f"s3://{bucket}/{chave}"


def processar(mensagem: dict, s3, sqs, url_saida: str, session: Session) -> None:
    """Salva o livro no S3, avisa na fila de saída e atualiza o banco."""
    livro = json.loads(mensagem["Body"])
    try:
        arquivo = salvar_livro(livro, s3)
        sqs.send_message(
            QueueUrl=url_saida,
            MessageBody=json.dumps({"id": livro["id"], "arquivo": arquivo}),
            MessageGroupId="livros",
            MessageDeduplicationId=livro["id"],
        )
    except Exception:
        atualizar_status(session, livro["id"], "erro")
        raise
    atualizar_status(session, livro["id"], "processado", arquivo)
    logger.info("Livro %s salvo em %s", livro["id"], arquivo)

def atualizar_status(
    session: Session, livro_id: str, status: str, arquivo: str | None = None
) -> None:
    """Atualiza o status (e o arquivo) do livro no banco."""
    livro = session.get(LivroDB, livro_id)
    if livro is None:
        logger.warning("Livro %s não está no banco, status não atualizado", livro_id)
        return
    livro.status = status
    if arquivo:
        livro.arquivo = arquivo
    session.add(livro)
    session.commit()


def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s"
    )
    engine = create_engine(DATABASE_URL)
    s3 = boto3.client("s3")
    sqs = boto3.client("sqs")
    url_entrada = sqs.get_queue_url(QueueName=NOME_FILA_ENTRADA)["QueueUrl"]
    url_saida = sqs.get_queue_url(QueueName=NOME_FILA_SAIDA)["QueueUrl"]
    logger.info("Worker iniciado, esperando mensagens")

    while True:
        resposta = sqs.receive_message(
            QueueUrl=url_entrada, MaxNumberOfMessages=10, WaitTimeSeconds=20
        )
        for mensagem in resposta.get("Messages", []):
            try:
                with Session(engine) as session:
                    processar(mensagem, s3, sqs, url_saida, session)
            except json.JSONDecodeError:
                logger.error("JSON inválido, descartando: %s", mensagem["Body"])
            except Exception:
                logger.exception("Erro ao processar, a mensagem volta para a fila")
                continue
            sqs.delete_message(
                QueueUrl=url_entrada, ReceiptHandle=mensagem["ReceiptHandle"]
            )


if __name__ == "__main__":
    main()