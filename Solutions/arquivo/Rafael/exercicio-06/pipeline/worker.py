import json
import logging
import time

from sqlmodel import Session

from pipeline import aws, db
from pipeline.config import get_settings
from pipeline.processing import binarizar

log = logging.getLogger("worker")


def processar_mensagem(mensagem: dict, session: Session) -> None:
    settings = get_settings()
    dados = json.loads(mensagem["Body"])
    image_id = dados["image_id"]
    chave = dados["chave"]
    try:
        original = aws.ler_objeto(settings.input_bucket, chave)
        resultado = binarizar(original)
        chave_saida = f"processed/{image_id}.png"
        aws.salvar_objeto(settings.output_bucket, chave_saida, resultado)
        db.marcar_processada(session, image_id, chave_saida)
        aws.enviar_mensagem(
            settings.processed_queue,
            json.dumps({"image_id": image_id, "chave": chave_saida}),
        )
    except Exception as erro:
        log.exception("Falha ao processar %s", image_id)
        db.marcar_erro(session, image_id, str(erro))
        raise
    aws.apagar_mensagem(settings.input_queue, mensagem["ReceiptHandle"])


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    settings = get_settings()
    db.init_db()
    log.info("Worker aguardando mensagens em %s", settings.input_queue)
    while True:
        try:
            mensagens = aws.receber_mensagens(settings.input_queue, espera=20)
        except Exception:
            log.exception("Erro ao ler a fila, tentando de novo")
            time.sleep(3)
            continue
        for mensagem in mensagens:
            with Session(db.get_engine()) as session:
                try:
                    processar_mensagem(mensagem, session)
                    log.info("Mensagem processada com sucesso.")
                except Exception as erro:
                    log.warning("Falha ao processar mensagem (%s).", erro)


if __name__ == "__main__":
    main()
