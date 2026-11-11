import os
from datetime import UTC, datetime

from sqlmodel import Field, Session, SQLModel, create_engine

# Se estiver a correr localmente, usa localhost; se estiver no docker, usa db
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/app_db"
)
engine = create_engine(DATABASE_URL)


class Livro(SQLModel, table=True):
    __tablename__ = "livros"

    id: str = Field(primary_key=True)
    titulo: str
    genero: str
    status: str = Field(default="recebido")
    arquivo: str | None = None
    criado_em: datetime = Field(default_factory=lambda: datetime.now(UTC))
    atualizado_em: datetime = Field(default_factory=lambda: datetime.now(UTC))


def criar_tabelas():
    SQLModel.metadata.create_all(engine)
    print("Tabelas criadas com sucesso na base de dados")


def obter_sessao():
    with Session(engine) as session:
        yield session


if __name__ == "__main__":
    print("A criar tabelas...")
    criar_tabelas()
