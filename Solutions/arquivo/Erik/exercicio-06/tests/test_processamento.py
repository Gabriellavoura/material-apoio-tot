import cv2
import numpy as np
import pytest

from app.processamento import binarizar


def _png_com_degrade() -> bytes:
    imagem = np.tile(np.arange(256, dtype=np.uint8), (64, 1))
    _, buffer = cv2.imencode(".png", imagem)
    return buffer.tobytes()


def test_binarizar_gera_apenas_preto_e_branco():
    resultado = binarizar(_png_com_degrade())

    dados = np.frombuffer(resultado, dtype=np.uint8)
    imagem = cv2.imdecode(dados, cv2.IMREAD_GRAYSCALE)
    assert set(np.unique(imagem)) <= {0, 255}


def test_binarizar_rejeita_conteudo_invalido():
    with pytest.raises(ValueError):
        binarizar(b"isso nao e uma imagem")