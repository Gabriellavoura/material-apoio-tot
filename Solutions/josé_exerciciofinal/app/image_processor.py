import cv2
import numpy as np

def binarize_image(image_bytes):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img_np = cv2.imdecode(nparr, cv2.IMREAD_GRAYSCALE)
    _, binarized = cv2.threshold(img_np, 127, 255, cv2.THRESH_BINARY)
    _, buffer = cv2.imencode('.png', binarized)
    return buffer.tobytes()
