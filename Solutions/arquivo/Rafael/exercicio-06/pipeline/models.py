import uuid
from datetime import UTC, datetime
from enum import Enum

from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel


class StatusImagem(str, Enum):
    RECEBIDA = "recebida"
    PROCESSADA = "processada"
    ERRO = "erro"


def agora() -> datetime:
    return datetime.now(UTC)


class Imagem(SQLModel, table=True):
    __tablename__ = "images"

    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    nome_arquivo: str
    status: StatusImagem = Field(default=StatusImagem.RECEBIDA, index=True)
    chave_entrada: str
    chave_saida: str | None = None
    erro: str | None = None
    enviada_em: datetime = Field(default_factory=agora, sa_type=DateTime(timezone=True))
    concluida_em: datetime | None = Field(default=None, sa_type=DateTime(timezone=True))