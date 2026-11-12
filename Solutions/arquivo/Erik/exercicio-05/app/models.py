from datetime import UTC, datetime

from sqlmodel import Field, SQLModel


def agora() -> datetime:
    return datetime.now(UTC)


class LivroDB(SQLModel, table=True):
    """Linha da tabela `livros`: guarda o status de cada livro recebido."""

    __tablename__ = "livros"

    id: str = Field(primary_key=True)
    titulo: str
    genero: str
    status: str = "recebido"
    arquivo: str | None = None
    criado_em: datetime = Field(default_factory=agora)
    atualizado_em: datetime = Field(
        default_factory=agora, sa_column_kwargs={"onupdate": agora}
    )