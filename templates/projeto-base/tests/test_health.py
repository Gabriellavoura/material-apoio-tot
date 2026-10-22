from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_retorna_ok():
    resposta = client.get("/health")

    assert resposta.status_code == 200
    assert resposta.json() == {"status": "ok"}
