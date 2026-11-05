import json
import logging
import tempfile
import time
from datetime import UTC, datetime

import cv2
from sqlmodel import Session

from app.aws import buscar_url_da_fila, criar_cliente_s3, criar_cliente_sqs
from app.database import engine
from app.models import Image, Livro, StatusImagem, StatusLivro

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def escolher_bucket(genero: str) -> str:
    if genero == "romance":
        return "romance"
    if genero == "ficcao":
        return "ficcao"
    return "outros"


def nome_do_arquivo(titulo: str) -> str:
    seguro = "".join(caractere for caractere in titulo if caractere.isalnum() or caractere in " -_")
    return f"{seguro.strip()}.json"


def processar_livro(livro: dict) -> None:
    bucket = escolher_bucket(livro["genero"])
    arquivo = nome_do_arquivo(livro["titulo"])

    criar_cliente_s3().put_object(
        Bucket=bucket,
        Key=arquivo,
        Body=json.dumps(livro, ensure_ascii=False),
        ContentType="application/json",
    )

    criar_cliente_sqs().send_message(
        QueueUrl=buscar_url_da_fila("livros-saida.fifo"),
        MessageBody=json.dumps({"id": livro["id"], "arquivo": f"s3://{bucket}/{arquivo}"}),
        MessageGroupId="livros",
        MessageDeduplicationId=f"saida-{livro['id']}",
    )

    with Session(engine) as session:
        registro = session.get(Livro, livro["id"])
        if registro:
            registro.status = StatusLivro.PROCESSADO
            registro.arquivo = f"s3://{bucket}/{arquivo}"
            registro.atualizado_em = datetime.now(UTC)
            session.add(registro)
            session.commit()


def processar_imagem(caminho_entrada: str, caminho_saida: str) -> None:
    imagem = cv2.imread(caminho_entrada)
    if imagem is None:
        raise ValueError("Não foi possível ler a imagem")

    cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
    _, binaria = cv2.threshold(
        cinza,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU,
    )
    if not cv2.imwrite(caminho_saida, binaria):
        raise ValueError("Não foi possível salvar a imagem processada")


def processar_mensagem_imagem(payload: dict) -> None:
    image_id = payload["id"]
    filename = payload["arquivo"]
    s3 = criar_cliente_s3()

    resposta = s3.get_object(Bucket="image-input", Key=filename)
    with tempfile.TemporaryDirectory() as diretorio:
        entrada = f"{diretorio}/entrada.png"
        saida = f"{diretorio}/saida.png"

        with open(entrada, "wb") as arquivo:
            arquivo.write(resposta["Body"].read())

        processar_imagem(entrada, saida)
        arquivo_saida = filename

        with open(saida, "rb") as arquivo:
            s3.put_object(Bucket="image-output", Key=arquivo_saida, Body=arquivo.read())

    with Session(engine) as session:
        registro = session.get(Image, image_id)
        if registro:
            registro.status = StatusImagem.PROCESSADA
            registro.arquivo_saida = arquivo_saida
            registro.concluida_em = datetime.now(UTC)
            session.add(registro)
            session.commit()

    criar_cliente_sqs().send_message(
        QueueUrl=buscar_url_da_fila("new-image-processed.fifo"),
        MessageBody=json.dumps({"id": image_id, "arquivo": arquivo_saida}),
        MessageGroupId="imagens",
        MessageDeduplicationId=f"processada-{image_id}",
    )


def marcar_erro(payload: dict, erro: Exception) -> None:
    with Session(engine) as session:
        registro = session.get(Image, payload["id"])
        if registro:
            registro.status = StatusImagem.ERRO
            registro.error = str(erro)
            session.add(registro)
            session.commit()


def executar() -> None:
    sqs = criar_cliente_sqs()

    while True:
        livros = sqs.receive_message(
            QueueUrl=buscar_url_da_fila("livros-entrada.fifo"),
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20,
        )
        imagens = sqs.receive_message(
            QueueUrl=buscar_url_da_fila("new-image-input.fifo"),
            MaxNumberOfMessages=1,
            WaitTimeSeconds=20,
        )

        for mensagem in livros.get("Messages", []):
            try:
                processar_livro(json.loads(mensagem["Body"]))
                sqs.delete_message(
                    QueueUrl=buscar_url_da_fila("livros-entrada.fifo"),
                    ReceiptHandle=mensagem["ReceiptHandle"],
                )
            except Exception:
                logger.exception("Falha ao processar livro")

        for mensagem in imagens.get("Messages", []):
            payload = None
            try:
                payload = json.loads(mensagem["Body"])
                processar_mensagem_imagem(payload)
                sqs.delete_message(
                    QueueUrl=buscar_url_da_fila("new-image-input.fifo"),
                    ReceiptHandle=mensagem["ReceiptHandle"],
                )
            except Exception as erro:
                logger.exception("Falha ao processar imagem")
                if payload:
                    marcar_erro(payload, erro)

        time.sleep(0.1)


if __name__ == "__main__":
    executar()
