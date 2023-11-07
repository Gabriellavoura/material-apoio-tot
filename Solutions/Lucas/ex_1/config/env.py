import os

AWS_HOST           = os.getenv('AWS_HOST', 'http://172.17.0.3:4566')
SQS_URL            = os.getenv('SQS_URL', 'http://172.17.0.3:4566/000000000000/InputQueue.fifo')
AWS_DEFAULT_REGION = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')

AWS_KEY    = os.getenv('AWS_KEY', 'localstack') 
AWS_SECRET = os.getenv('AWS_SECRET', 'localstack')