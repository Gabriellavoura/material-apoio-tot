import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    
    # AWS/LocalStack
    AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID', 'test')
    AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', 'test')
    AWS_REGION = os.environ.get('AWS_REGION', 'us-east-1')
    AWS_ENDPOINT_URL = os.environ.get('AWS_ENDPOINT_URL', 'http://localhost:4566')
    
    # S3
    S3_INPUT_BUCKET = os.environ.get('S3_INPUT_BUCKET', 'image-input')
    S3_OUTPUT_BUCKET = os.environ.get('S3_OUTPUT_BUCKET', 'image-output')
    
    # SQS
    SQS_QUEUE_NAME = os.environ.get('SQS_QUEUE_NAME', 'new-image-input.fifo')
    SQS_MESSAGE_GROUP_ID = os.environ.get('SQS_MESSAGE_GROUP_ID', 'image-processing')
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # Worker
    WORKER_POLL_INTERVAL = int(os.environ.get('WORKER_POLL_INTERVAL', '5'))
    WORKER_MAX_MESSAGES = int(os.environ.get('WORKER_MAX_MESSAGES', '10'))

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}