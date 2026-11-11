from pipeline import db
from pipeline.models import ERRO, PROCESSADA, RECEBIDA


def test_imagem_nasce_como_recebida(session):
    imagem = db.criar_imagem(session, "id-1", "a.png", "id-1.png")
    assert imagem.status == RECEBIDA
    assert imagem.concluida_em is None


def test_marcar_processada(session):
    db.criar_imagem(session, "id-2", "b.png", "id-2.png")
    imagem = db.marcar_processada(session, "id-2", "processed/id-2.png")
    assert imagem.status == PROCESSADA
    assert imagem.chave_saida == "processed/id-2.png"
    assert imagem.concluida_em is not None


def test_marcar_erro(session):
    db.criar_imagem(session, "id-3", "c.png", "id-3.png")
    imagem = db.marcar_erro(session, "id-3", "falhou")
    assert imagem.status == ERRO
    assert imagem.erro == "falhou"


def test_listar_filtra_por_status(session):
    db.criar_imagem(session, "id-4", "d.png", "id-4.png")
    db.criar_imagem(session, "id-5", "e.png", "id-5.png")
    db.marcar_erro(session, "id-5", "x")
    assert [i.id for i in db.listar_imagens(session, ERRO)] == ["id-5"]
    assert len(db.listar_imagens(session)) == 2
