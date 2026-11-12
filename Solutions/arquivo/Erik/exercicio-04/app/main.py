"""API mínima: use este arquivo como ponto de partida dos exercícios."""

import boto3
from fastapi import FastAPI
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlmodel import Session, create_engine

from app.config import DATABASE_URL
from app.fila import enviar_livro

app = FastAPI(title="ToT - projeto base", version="0.1.0")
engine = create_engine(DATABASE_URL)
class Livro(BaseModel):
    """Dados de um livro enviado para a fila de entrada."""

    id: str = Field(description="Identificador único do livro", examples=["12345"])
    titulo: str = Field(description="Título do livro", examples=["LoremIpsum"])
    autor: str = Field(description="Nome do autor", examples=["John Doe"])
    ano: int = Field(description="Ano de publicação", examples=[1960])
    genero: str = Field(description="Gênero literário", examples=["romance"])
    resumo: str = Field(description="Resumo do livro")


@app.get("/health")
def health() -> dict:
    """Responde 200 quando a API está no ar."""
    return {"status": "ok"}


@app.get("/health/deps")
def health_deps() -> dict:
    """Testa a conexão com o Postgres e com o Floci (S3)."""
    with Session(engine) as session:
        session.exec(text("SELECT 1"))

    # O boto3 lê AWS_ENDPOINT_URL do ambiente e fala com o Floci, não com a AWS real.
    buckets = boto3.client("s3").list_buckets()["Buckets"]

    return {"postgres": "ok", "s3_buckets": [b["Name"] for b in buckets]}

@app.post(
    "/livros",
    status_code=202,
    summary="Envia um livro para processamento",
    description=(
        "Valida os dados do livro e envia para a fila `livros-entrada.fifo`. "
        "Responde 202 quando a mensagem é aceita e 422 se os dados forem inválidos."
    ),
)
def criar_livro(livro: Livro) -> dict:
    """Recebe um livro, valida e envia para a fila de entrada."""
    enviar_livro(livro.model_dump())
    return {"status": "aceito", "id": livro.id}