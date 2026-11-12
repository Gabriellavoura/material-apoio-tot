"""API dos exercicios de livros e imagens."""

import json
import uuid

import boto3
from fastapi import FastAPI, HTTPException, UploadFile, status
from fastapi.responses import JSONResponse
from sqlalchemy import text
from sqlmodel import Session, SQLModel, select

from app.aws import buscar_url_da_fila, criar_cliente_s3, criar_cliente_sqs
from app.database import engine
from app.models import Image, Livro
from app.schemas import LivroEntrada

SQLModel.metadata.create_all(engine)

app = FastAPI(
    title="ToT - onboarding",
    version="1.0.0",
    description="API do pipeline de livros e imagens com S3, SQS e PostgreSQL.",
)


@app.get("/health")
def health() -> dict:
    """Responde 200 quando a API está no ar."""
    return {"status": "ok"}


@app.post("/livros", status_code=status.HTTP_202_ACCEPTED, tags=["livros"])
def criar_livro(livro: LivroEntrada) -> dict:
    with Session(engine) as session:
        if session.get(Livro, livro.id):
            raise HTTPException(status_code=409, detail="Livro já existe")

        session.add(Livro(**livro.model_dump()))
        session.commit()

    criar_cliente_sqs().send_message(
        QueueUrl=buscar_url_da_fila("livros-entrada.fifo"),
        MessageBody=json.dumps(livro.model_dump(), ensure_ascii=False),
        MessageGroupId="livros",
        MessageDeduplicationId=livro.id,
    )
    return {"status": "recebido", "id": livro.id}


@app.get("/livros/{livro_id}", tags=["livros"])
def obter_livro(livro_id: str) -> Livro:
    with Session(engine) as session:
        livro = session.get(Livro, livro_id)
        if not livro:
            raise HTTPException(status_code=404, detail="Livro não encontrado")
        return livro


@app.get("/livros", tags=["livros"])
def listar_livros(status_livro: str | None = None) -> list[Livro]:
    with Session(engine) as session:
        consulta = select(Livro)
        if status_livro:
            consulta = consulta.where(Livro.status == status_livro)

        return list(session.exec(consulta).all())


@app.post("/images", status_code=status.HTTP_202_ACCEPTED, tags=["imagens"])
async def criar_imagem(arquivo: UploadFile) -> dict:
    # Por enquanto o pipeline trabalha apenas com PNG.
    if not arquivo.filename or not arquivo.filename.lower().endswith(".png"):
        return JSONResponse(
            status_code=400,
            content={"detail": "O arquivo deve estar no formato .png"},
        )

    image_id = str(uuid.uuid4())
    filename = f"{image_id}.png"
    conteudo = await arquivo.read()

    criar_cliente_s3().put_object(Bucket="image-input", Key=filename, Body=conteudo)

    with Session(engine) as session:
        session.add(
            Image(
                id=image_id,
                filename=arquivo.filename,
                arquivo_entrada=filename,
            )
        )
        session.commit()

    criar_cliente_sqs().send_message(
        QueueUrl=buscar_url_da_fila("new-image-input.fifo"),
        MessageBody=json.dumps({"id": image_id, "arquivo": filename}),
        MessageGroupId="imagens",
        MessageDeduplicationId=image_id,
    )
    return {"id": image_id, "status": "recebida"}


@app.get("/images/{image_id}", tags=["imagens"])
def obter_imagem(image_id: str) -> Image:
    with Session(engine) as session:
        imagem = session.get(Image, image_id)
        if not imagem:
            raise HTTPException(status_code=404, detail="Imagem não encontrada")
        return imagem


@app.get("/images", tags=["imagens"])
def listar_imagens(status_imagem: str | None = None) -> list[Image]:
    with Session(engine) as session:
        consulta = select(Image)
        if status_imagem:
            consulta = consulta.where(Image.status == status_imagem)
        return list(session.exec(consulta).all())


@app.get("/health/deps")
def health_deps() -> dict:
    """Testa a conexão com o Postgres e com o Floci (S3)."""
    with Session(engine) as session:
        session.exec(text("SELECT 1"))

    buckets = boto3.client("s3").list_buckets()["Buckets"]

    return {"postgres": "ok", "s3_buckets": [b["Name"] for b in buckets]}
