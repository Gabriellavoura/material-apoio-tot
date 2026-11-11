from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

def test_health():
    assert client.get("/health").status_code == 200

@patch("app.main.enviar_mensagem_livro")
def test_criar_livro(mock_enviar):
    dados = {
        "id": "123", "titulo": "Teste", "autor": "Rafael",
        "ano": 2024, "genero": "TI", "resumo": "Resumo"
    }
    assert client.post("/livros", json=dados).status_code == 202
    mock_enviar.assert_called_once()
