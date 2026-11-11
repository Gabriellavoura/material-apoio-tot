from datetime import UTC, datetime
from functools import lru_cache

from sqlalchemy import Engine
from sqlmodel import Session, SQLModel, create_engine, select

from pipeline.config import get_settings
from pipeline.models import ERRO, PROCESSADA, Imagem


@lru_cache
def get_engine() -> Engine:
    return create_engine(get_settings().database_url, pool_pre_ping=True)


def init_db(engine: Engine | None = None) -> None:
    SQLModel.metadata.create_all(engine or get_engine())


def criar_imagem(
    session: Session, image_id: str, nome_arquivo: str, chave_entrada: str
) -> Imagem:
    imagem = Imagem(id=image_id, nome_arquivo=nome_arquivo, chave_entrada=chave_entrada)
    session.add(imagem)
    session.commit()
    session.refresh(imagem)
    return imagem


def marcar_processada(session: Session, image_id: str, chave_saida: str) -> Imagem:
    imagem = session.get(Imagem, image_id)
    imagem.status = PROCESSADA
    imagem.chave_saida = chave_saida
    imagem.erro = None
    imagem.concluida_em = datetime.now(UTC)
    session.add(imagem)
    session.commit()
    session.refresh(imagem)
    return imagem


def marcar_erro(session: Session, image_id: str, mensagem: str) -> Imagem:
    imagem = session.get(Imagem, image_id)
    imagem.status = ERRO
    imagem.erro = mensagem
    imagem.concluida_em = datetime.now(UTC)
    session.add(imagem)
    session.commit()
    session.refresh(imagem)
    return imagem


def listar_imagens(session: Session, status: str | None = None) -> list[Imagem]:
    consulta = select(Imagem).order_by(Imagem.enviada_em.desc())
    if status:
        consulta = consulta.where(Imagem.status == status)
    return list(session.exec(consulta))
