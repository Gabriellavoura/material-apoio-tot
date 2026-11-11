import cv2
import numpy as np
import pytest

from pipeline.processing import binarizar


def test_binarizar_gera_apenas_preto_e_branco(png_bytes):
    resultado = binarizar(png_bytes)
    imagem = cv2.imdecode(np.frombuffer(resultado, np.uint8), cv2.IMREAD_GRAYSCALE)
    assert set(np.unique(imagem).tolist()) <= {0, 255}


def test_binarizar_rejeita_entrada_invalida():
    with pytest.raises(ValueError):
        binarizar(b"isso nao e uma imagem")
