from fastapi.testclient import TestClient

from app import main

client = TestClient(main.app)

LIVRO = {
    "id": "12345",
    "titulo": "LoremIpsum",
    "autor": "John Doe",
    "ano": 1960,
    "genero": "romance",
    "resumo": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
}


def test_criar_livro_retorna_202(monkeypatch):
    enviados = []
    monkeypatch.setattr(main, "enviar_livro", enviados.append)

    resposta = client.post("/livros", json=LIVRO)

    assert resposta.status_code == 202
    assert enviados == [LIVRO]


def test_criar_livro_com_ano_invalido_retorna_422():
    resposta = client.post("/livros", json={**LIVRO, "ano": "abc"})

    assert resposta.status_code == 422