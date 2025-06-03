"""
Input validation utilities
"""

import os
from werkzeug.datastructures import FileStorage

def validate_image_file(file):
    """
    Validate uploaded image file
    
    Args:
        file (FileStorage): Uploaded file object
        
    Returns:
        bool: True if valid PNG file, False otherwise
    """
    if not file or not file.filename:
        return False
    
    # Check file extension
    if not file.filename.lower().endswith('.png'):
        return False
    
    # Check if file has content
    if file.content_length == 0:
        return False
    
    # Check MIME type if available
    if hasattr(file, 'content_type') and file.content_type:
        if not file.content_type.startswith('image/'):
            return False
    
    return True

def validate_file_size(file, max_size_mb=16):
    """
    Validate file size
    
    Args:
        file (FileStorage): Uploaded file object
        max_size_mb (int): Maximum file size in MB
        
    Returns:
        bool: True if file size is within limits, False otherwise
    """
    if not file:
        return False
    
    max_size_bytes = max_size_mb * 1024 * 1024
    
    if hasattr(file, 'content_length') and file.content_length:
        return file.content_length <= max_size_bytes
    
    # If content_length is not available, read the file to check size
    file.seek(0, os.SEEK_END)
    size = file.tell()
    file.seek(0)  # Reset file pointer
    
    return size <= max_size_bytes

def validate_image_dimensions(image_data, max_width=4096, max_height=4096):
    """
    Validate image dimensions
    
    Args:
        image_data (bytes): Image data
        max_width (int): Maximum allowed width
        max_height (int): Maximum allowed height
        
    Returns:
        bool: True if dimensions are within limits, False otherwise
    """
    try:
        from PIL import Image
        import io
        
        # Open image from bytes
        img = Image.open(io.BytesIO(image_data))
        width, height = img.size
        
        return width <= max_width and height <= max_height
        
    except Exception:
        return False
    
    
    
def validate_png_file(file: FileStorage) -> dict:
    """
    Validate that the uploaded file is a valid PNG image
    
    Args:
        file: FileStorage object from Flask request
        
    Returns:
        dict: {'valid': bool, 'error': str}
    """
    
    # Check if filename is empty
    if not file.filename or file.filename == '':
        return {'valid': False, 'error': 'No file selected'}
    
    # Check file extension
    if not file.filename.lower().endswith('.png'):
        return {'valid': False, 'error': 'Invalid file type, only PNG images are allowed'}
    
    # Check file size (basic check)
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)  # Reset file pointer
    
    if file_size == 0:
        return {'valid': False, 'error': 'File is empty'}
    
    # Check PNG magic bytes
    magic_bytes = file.read(8)
    file.seek(0)  # Reset file pointer
    
    png_signature = b'\x89PNG\r\n\x1a\n'
    if magic_bytes != png_signature:
        return {'valid': False, 'error': 'File is not a valid PNG image'}
    
    return {'valid': True, 'error': None}

def validate_image_id(image_id: str) -> bool:
    """
    Validate that the image ID is a valid UUID
    
    Args:
        image_id: String to validate
        
    Returns:
        bool: True if valid UUID, False otherwise
    """
    import uuid
    
    try:
        uuid.UUID(image_id)
        return True
    except ValueError:
        return False