from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


def agora() -> datetime:
    return datetime.now(UTC)


class ImagemDB(SQLModel, table=True):
    """Linha da tabela `images`: acompanha cada imagem enviada."""

    __tablename__ = "images"

    id: str = Field(primary_key=True)
    nome_original: str
    status: str = "recebida"
    erro: str | None = None
    enviado_em: datetime = Field(default_factory=agora)
    concluido_em: datetime | None = None