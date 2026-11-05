from datetime import UTC, datetime
from enum import Enum

from sqlmodel import Field, SQLModel


def utcnow() -> datetime:
    return datetime.now(UTC)


class StatusLivro(str, Enum):
    RECEBIDO = "recebido"
    PROCESSADO = "processado"
    ERRO = "erro"


class StatusImagem(str, Enum):
    RECEBIDA = "recebida"
    PROCESSADA = "processada"
    ERRO = "erro"


class Livro(SQLModel, table=True):
    id: str = Field(primary_key=True)
    titulo: str
    autor: str
    ano: int
    genero: str
    resumo: str
    status: StatusLivro = StatusLivro.RECEBIDO
    arquivo: str | None = None
    criado_em: datetime = Field(default_factory=utcnow)
    atualizado_em: datetime = Field(default_factory=utcnow)


class Image(SQLModel, table=True):
    id: str = Field(primary_key=True)
    filename: str
    status: StatusImagem = StatusImagem.RECEBIDA
    error: str | None = None
    arquivo_entrada: str
    arquivo_saida: str | None = None
    enviada_em: datetime = Field(default_factory=utcnow)
    concluida_em: datetime | None = None
