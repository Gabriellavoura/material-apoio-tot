from app.worker import escolher_bucket, nome_arquivo


def test_escolher_bucket_romance():
    assert escolher_bucket("romance") == "romance"


def test_escolher_bucket_desconhecido_vai_para_outros():
    assert escolher_bucket("terror") == "outros"


def test_nome_arquivo():
    assert nome_arquivo({"titulo": "LoremIpsum"}) == "LoremIpsum.json"