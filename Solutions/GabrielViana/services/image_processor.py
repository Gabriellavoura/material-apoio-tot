
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    def __init__(self):
        """Initialize image processor"""
        pass
    
    def process_image(self, image_data):
        """
        Process image by applying binarization using OpenCV
        
        Args:
            image_data (bytes): Raw image data
            
        Returns:
            bytes
        """
        
        
        try:
            # Convert bytes to numpy array
            nparr = np.frombuffer(image_data, np.uint8)
            # Decode image
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
            
            if img is None:
                logger.error("Failed to decode image")
                return None
            
            # Convert to grayscale
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            # Apply binary thresholding
            _, binary = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
            
            # Encode processed image back to bytes
            _, buffer = cv2.imencode('.png', binary)
            processed_image_data = buffer.tobytes()
            
            return processed_image_data
        except Exception as e:
            logger.error(f"Error processing image: {str(e)}")
            return None
            