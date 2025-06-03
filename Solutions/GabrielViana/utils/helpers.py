import logging
from flask import Flask

def setup_logging(app: Flask):
    """Setup logging configuration for the application"""
    
    # Set log level from config
    log_level = getattr(logging, app.config.get('LOG_LEVEL', 'INFO').upper())
    app.logger.setLevel(log_level)
    
    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    
    # Add handler to app logger
    app.logger.addHandler(console_handler)
    
    # Prevent duplicate logs
    app.logger.propagate = False

def create_directories():
    """Create necessary directories if they don't exist"""
    import os
    
    directories = ['temp']
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created directory: {directory}")