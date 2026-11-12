import boto3
import pytest
from fastapi.testclient import TestClient
from moto import mock_aws
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
def salvos(monkeypatch):
    """Substitui o envio ao S3 e guarda o que seria salvo."""
    lista = []
    monkeypatch.setattr(
        main, "salvar_imagem", lambda chave, conteudo: lista.append((chave, conteudo))
    )
    return lista


@pytest.fixture
def enviados(monkeypatch):
    """Substitui o aviso à fila e guarda o que seria enviado."""
    lista = []
    monkeypatch.setattr(
        main, "enviar_imagem", lambda imagem_id, chave: lista.append((imagem_id, chave))
    )
    return lista


@pytest.fixture
def client(session, salvos, enviados):
    main.app.dependency_overrides[main.get_session] = lambda: session
    yield TestClient(main.app)
    main.app.dependency_overrides.clear()

@pytest.fixture
def aws(monkeypatch):
    """AWS simulada em memória, com os buckets e as filas do projeto."""
    monkeypatch.delenv("AWS_ENDPOINT_URL", raising=False)
    monkeypatch.setenv("AWS_DEFAULT_REGION", "us-east-1")
    monkeypatch.setenv("AWS_ACCESS_KEY_ID", "test")
    monkeypatch.setenv("AWS_SECRET_ACCESS_KEY", "test")
    with mock_aws():
        s3 = boto3.client("s3")
        s3.create_bucket(Bucket="image-input")
        s3.create_bucket(Bucket="image-output")
        sqs = boto3.client("sqs")
        for nome in ("new-image-input.fifo", "new-image-processed.fifo"):
            sqs.create_queue(QueueName=nome, Attributes={"FifoQueue": "true"})
        yield