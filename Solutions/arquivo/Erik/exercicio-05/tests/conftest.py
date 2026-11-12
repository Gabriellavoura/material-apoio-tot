import pytest
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

from app import main


@pytest.fixture
def session():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture
def enviados(monkeypatch):
    """Substitui o envio para a fila e guarda o que seria enviado."""
    lista = []
    monkeypatch.setattr(main, "enviar_livro", lista.append)
    return lista


@pytest.fixture
def client(session, enviados):
    main.app.dependency_overrides[main.get_session] = lambda: session
    yield TestClient(main.app)
    main.app.dependency_overrides.clear()