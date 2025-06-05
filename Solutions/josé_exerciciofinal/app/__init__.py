from flask import Flask
from flask_restx import Api
from app.routes import api as image_api


api = Api(
    title="Image Pipeline API",
    version="1.0",
    description="API para pipeline de processamento de imagens com S3 e SQS"
)

def create_app():
    app = Flask(__name__)
    api.init_app(app)

    from .routes import api as image_api
    api.add_namespace(image_api)

    return app
