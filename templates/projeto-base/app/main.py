"""API mínima: use este arquivo como ponto de partida dos exercícios."""

import boto3
from fastapi import FastAPI
from sqlalchemy import text
from sqlmodel import Session, create_engine

from app.config import DATABASE_URL

app = FastAPI(title="ToT - projeto base", version="0.1.0")
engine = create_engine(DATABASE_URL)


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
