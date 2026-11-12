"""API mínima: use este arquivo como ponto de partida dos exercícios."""

from contextlib import asynccontextmanager
from typing import Annotated

import boto3
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine, select

from app import models  # noqa: F401  (registra a tabela no SQLModel)
from app.config import DATABASE_URL
from app.fila import enviar_livro
from app.models import LivroDB

engine = create_engine(DATABASE_URL)


@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="ToT - projeto base", version="0.1.0", lifespan=lifespan)
def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]
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
def criar_livro(livro: Livro, session: SessionDep) -> dict:
    if session.get(LivroDB, livro.id):
        raise HTTPException(status_code=409, detail="Livro já cadastrado")

    session.add(LivroDB(id=livro.id, titulo=livro.titulo, genero=livro.genero))
    session.commit()

    enviar_livro(livro.model_dump())
    return {"status": "aceito", "id": livro.id}

@app.get(
    "/livros/{id}",
    response_model=LivroDB,
    summary="Consulta um livro",
    description="Devolve os dados e o status do livro, ou 404 se ele não existir.",
)
def buscar_livro(id: str, session: SessionDep) -> LivroDB:
    livro = session.get(LivroDB, id)
    if not livro:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return livro


@app.get(
    "/livros",
    response_model=list[LivroDB],
    summary="Lista os livros",
    description="Lista os livros. Use `?status=processado` para filtrar pelo status.",
)
def listar_livros(session: SessionDep, status: str | None = None) -> list[LivroDB]:
    consulta = select(LivroDB)
    if status:
        consulta = consulta.where(LivroDB.status == status)
    return session.exec(consulta).all()