from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.exercicio_05 import obter_sessao
from app.main import app

engine_test = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)


@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine_test)
    with Session(engine_test) as session:
        yield session
    SQLModel.metadata.drop_all(engine_test)


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[obter_sessao] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()




def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200


@patch("app.main.enviar_mensagem_livro")
def test_criar_livro(mock_enviar, client):
    dados = {
        "id": "123",
        "titulo": "Teste",
        "autor": "Rafael",
        "ano": 2024,
        "genero": "TI",
        "resumo": "Resumo",
    }
    response = client.post("/livros", json=dados)
    assert response.status_code == 202
    mock_enviar.assert_called_once()