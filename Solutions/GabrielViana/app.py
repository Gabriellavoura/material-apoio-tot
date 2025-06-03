import os
from flask import Flask
from flask_restx import Api

from config.settings import config
from api.models.swagger_models import create_swagger_models
from api.middlewares.error_handlers import register_error_handlers
from api.routes.upload import create_upload_routes
from api.routes.health import create_health_routes
from api.routes.process import create_process_routes
from services.sqs_worker import start_background_worker
from utils.helpers import setup_logging, create_directories

def create_app(config_name=None):
    app = Flask(__name__)
    
    config_name = config_name or os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config[config_name])
    
    setup_logging(app)
    create_directories()
    

    api = Api(
        app,
        version='1.0',
        title='API Material de apoio ToT',
        description='API para upload e processamento de imagens',
        doc='/docs/'
    )
    
    models = create_swagger_models(api)
    
    # Namespaces for api routes
    upload_ns = api.namespace('upload', description='Rota de upload de imagens')
    health_ns = api.namespace('health', description='Health check')
    process_ns = api.namespace('process', description='Worker status')
    
    # ROUTE REGISTRATION SECTION
    create_upload_routes(api, upload_ns, models)
    create_health_routes(api, health_ns, models)
    create_process_routes(api, process_ns, models)
    #

    register_error_handlers(app)
    
    return app

def main():
    app = create_app()
    start_background_worker(app)
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=app.config.get('DEBUG', False),
        threaded=True
    )

if __name__ == '__main__':
    main()