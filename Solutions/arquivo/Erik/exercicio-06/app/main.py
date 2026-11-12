"""API mínima: use este arquivo como ponto de partida dos exercícios."""

from contextlib import asynccontextmanager
from typing import Annotated
from uuid import uuid4

import boto3
from fastapi import Depends, FastAPI, HTTPException, UploadFile
from sqlalchemy import text
from sqlmodel import Session, SQLModel, create_engine, select

from app import models  # noqa: F401  (registra a tabela no SQLModel)
from app.armazenamento import salvar_imagem
from app.config import DATABASE_URL
from app.fila import enviar_imagem
from app.models import ImagemDB

engine = create_engine(DATABASE_URL)

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(title="ToT - projeto base", version="0.1.0", lifespan=lifespan)

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

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

@app.post(
    "/images",
    status_code=202,
    summary="Envia uma imagem para processamento",
    description=(
        "Recebe um arquivo `.png`, guarda no S3, registra no banco com status "
        "`recebida` e avisa o worker pela fila. Responde 202 com o `id` da imagem."
    ),
    responses={415: {"description": "O arquivo enviado não é um .png"}},
)
def criar_imagem(arquivo: UploadFile, session: SessionDep) -> dict:
    nome = arquivo.filename or ""
    if not nome.lower().endswith(".png"):
        raise HTTPException(status_code=415, detail="Envie um arquivo .png")

    imagem_id = str(uuid4())
    chave = f"{imagem_id}.png"

    salvar_imagem(chave, arquivo.file.read())
    session.add(ImagemDB(id=imagem_id, nome_original=nome))
    session.commit()
    enviar_imagem(imagem_id, chave)

    return {"id": imagem_id, "status": "recebida"}

@app.get(
    "/images/{id}",
    response_model=ImagemDB,
    summary="Consulta uma imagem",
    description="Devolve o status e as datas de envio e de conclusão da imagem.",
    responses={404: {"description": "Imagem não encontrada"}},
)
def buscar_imagem(id: str, session: SessionDep) -> ImagemDB:
    imagem = session.get(ImagemDB, id)
    if not imagem:
        raise HTTPException(status_code=404, detail="Imagem não encontrada")
    return imagem


@app.get(
    "/images",
    response_model=list[ImagemDB],
    summary="Lista as imagens",
    description=(
        "Lista as imagens enviadas. Use `?status=processada` para filtrar "
        "(`recebida`, `processada` ou `erro`)."
    ),
)
def listar_imagens(session: SessionDep, status: str | None = None) -> list[ImagemDB]:
    consulta = select(ImagemDB)
    if status:
        consulta = consulta.where(ImagemDB.status == status)
    return session.exec(consulta).all()