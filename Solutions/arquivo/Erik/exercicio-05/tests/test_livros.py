from app.models import LivroDB

LIVRO = {
    "id": "12345",
    "titulo": "LoremIpsum",
    "autor": "John Doe",
    "ano": 1960,
    "genero": "romance",
    "resumo": "Lorem ipsum dolor sit amet, consectetur adipiscing elit.",
}


def test_criar_livro_retorna_202(client, session, enviados):
    resposta = client.post("/livros", json=LIVRO)

    assert resposta.status_code == 202
    assert enviados == [LIVRO]
    assert session.get(LivroDB, "12345").status == "recebido"


def test_criar_livro_repetido_retorna_409(client, enviados):
    client.post("/livros", json=LIVRO)
    resposta = client.post("/livros", json=LIVRO)

    assert resposta.status_code == 409
    assert len(enviados) == 1


def test_criar_livro_com_ano_invalido_retorna_422(client):
    resposta = client.post("/livros", json={**LIVRO, "ano": "abc"})

    assert resposta.status_code == 422


def test_buscar_livro_retorna_200(client):
    client.post("/livros", json=LIVRO)
    resposta = client.get("/livros/12345")

    assert resposta.status_code == 200
    assert resposta.json()["status"] == "recebido"


def test_buscar_livro_inexistente_retorna_404(client):
    resposta = client.get("/livros/nao-existe")

    assert resposta.status_code == 404


def test_listar_livros_filtra_por_status(client):
    client.post("/livros", json=LIVRO)

    assert len(client.get("/livros").json()) == 1
    assert len(client.get("/livros", params={"status": "recebido"}).json()) == 1
    assert client.get("/livros", params={"status": "processado"}).json() == []