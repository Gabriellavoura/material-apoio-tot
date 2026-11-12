import cv2
import numpy as np
from fastapi.testclient import TestClient

from app.main import app
from app.worker import escolher_bucket, nome_do_arquivo, processar_imagem

client = TestClient(app)


def test_generos_conhecidos_usam_seus_buckets():
    assert escolher_bucket("romance") == "romance"
    assert escolher_bucket("ficcao") == "ficcao"
    assert escolher_bucket("biografia") == "outros"


def test_titulo_com_espacos_vira_nome_de_json():
    assert nome_do_arquivo("Dom Casmurro") == "Dom Casmurro.json"


def test_imagem_branca_pode_ser_binarizada(tmp_path):
    entrada = tmp_path / "entrada.png"
    saida = tmp_path / "saida.png"
    cv2.imwrite(str(entrada), np.full((20, 20, 3), 255, dtype=np.uint8))
    processar_imagem(str(entrada), str(saida))
    assert saida.exists()


def test_upload_aceita_png_e_rejeita_outro_formato(monkeypatch):
    class FakeS3:
        def put_object(self, **kwargs):
            return None

    class FakeSQS:
        def send_message(self, **kwargs):
            return None

    monkeypatch.setattr("app.main.criar_cliente_s3", lambda: FakeS3())
    monkeypatch.setattr("app.main.criar_cliente_sqs", lambda: FakeSQS())
    monkeypatch.setattr("app.main.buscar_url_da_fila", lambda nome: nome)
    valida = client.post(
        "/images",
        files={"arquivo": ("teste.png", b"\x89PNG\r\n", "image/png")},
    )
    assert valida.status_code == 202

    invalida = client.post(
        "/images",
        files={"arquivo": ("teste.txt", b"texto", "text/plain")},
    )
    assert invalida.status_code == 400
