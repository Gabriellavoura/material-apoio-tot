import cv2
import numpy as np
from io import BytesIO

def process_image(image_bytes: bytes) -> BytesIO:
    # Converte os bytes para numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    # Converte para grayscale e aplica binarização
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

    # Codifica a imagem como PNG e retorna como BytesIO
    _, buffer = cv2.imencode('.png', binary)
    return BytesIO(buffer)
