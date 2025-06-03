import uuid
from io import BytesIO

import numpy as np
from PIL import Image


class TestUtils:
    def generate_random_images():
        frontal_image = np.random.uniform(0, 1, (256, 256, 3)).astype(np.float32)
        side_image = np.random.uniform(0, 1, (256, 256, 3)).astype(np.float32)

        frontal_image = Image.fromarray((frontal_image * 255).astype(np.uint8))
        side_image = Image.fromarray((side_image * 255).astype(np.uint8))
        buffer = BytesIO()

        frontal_image.save(buffer, format="PNG")
        frontal_image = buffer.getvalue()

        buffer = BytesIO()
        side_image.save(buffer, format="PNG")
        side_image = buffer.getvalue()

        return frontal_image, side_image