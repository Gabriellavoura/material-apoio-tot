from app.models import ImagemDB


def test_upload_png_retorna_202(client, session, salvos, enviados):
    resposta = client.post(
        "/images", files={"arquivo": ("foto.png", b"conteudo", "image/png")}
    )

    assert resposta.status_code == 202
    imagem_id = resposta.json()["id"]
    assert session.get(ImagemDB, imagem_id).status == "recebida"
    assert salvos == [(f"{imagem_id}.png", b"conteudo")]
    assert enviados == [(imagem_id, f"{imagem_id}.png")]


def test_upload_que_nao_e_png_retorna_415(client, session, salvos, enviados):
    resposta = client.post(
        "/images", files={"arquivo": ("texto.txt", b"oi", "text/plain")}
    )

    assert resposta.status_code == 415
    assert salvos == []
    assert enviados == []


def test_buscar_imagem_inexistente_retorna_404(client):
    assert client.get("/images/nao-existe").status_code == 404


def test_listar_imagens_filtra_por_status(client):
    client.post("/images", files={"arquivo": ("foto.png", b"x", "image/png")})

    assert len(client.get("/images").json()) == 1
    assert len(client.get("/images", params={"status": "recebida"}).json()) == 1
    assert client.get("/images", params={"status": "processada"}).json() == []