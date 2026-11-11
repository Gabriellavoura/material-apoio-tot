import pytest
from fastapi.testclient import TestClient

from pipeline import api


@pytest.fixture
def client(session, monkeypatch):
    salvos = []
    enviadas = []
    monkeypatch.setattr(
        api.aws,
        "salvar_objeto",
        lambda bucket, chave, conteudo: salvos.append((bucket, chave)),
    )
    monkeypatch.setattr(
        api.aws,
        "enviar_mensagem",
        lambda fila, corpo, grupo="imagens": enviadas.append((fila, corpo)),
    )
    api.app.dependency_overrides[api.get_session] = lambda: session
    cliente = TestClient(api.app)
    cliente.salvos = salvos
    cliente.enviadas = enviadas
    yield cliente
    api.app.dependency_overrides.clear()


def test_health(client):
    assert client.get("/health").status_code == 200


def test_upload_png_valido(client, png_bytes):
    resposta = client.post("/images", files={"file": ("a.png", png_bytes, "image/png")})
    assert resposta.status_code == 202
    image_id = resposta.json()["id"]
    assert len(client.salvos) == 1
    assert len(client.enviadas) == 1
    consulta = client.get(f"/images/{image_id}")
    assert consulta.status_code == 200
    assert consulta.json()["status"] == "recebida"


def test_upload_extensao_invalida(client):
    resposta = client.post("/images", files={"file": ("a.txt", b"oi", "text/plain")})
    assert resposta.status_code == 400
    assert "png" in resposta.json()["detail"].lower()
    assert client.enviadas == []


def test_upload_png_falso(client):
    resposta = client.post(
        "/images", files={"file": ("a.png", b"nao e png", "image/png")}
    )
    assert resposta.status_code == 400


def test_imagem_inexistente(client):
    assert client.get("/images/nao-existe").status_code == 404


def test_listar_com_filtro(client, png_bytes):
    client.post("/images", files={"file": ("a.png", png_bytes, "image/png")})
    assert len(client.get("/images?status=recebida").json()) == 1
    assert client.get("/images?status=erro").json() == []
