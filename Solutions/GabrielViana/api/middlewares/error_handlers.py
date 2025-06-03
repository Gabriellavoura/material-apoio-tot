from flask import jsonify
from datetime import datetime
import logging

def register_error_handlers(app):
    """Register global error handlers for the Flask app"""
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'error': 'Bad request',
            'timestamp': datetime.utcnow().isoformat()
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'error': 'Resource not found',
            'timestamp': datetime.utcnow().isoformat()
        }), 404

    @app.errorhandler(413)
    def payload_too_large(error):
        return jsonify({
            'error': 'File too large',
            'timestamp': datetime.utcnow().isoformat()
        }), 413

    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Internal server error: {str(error)}")
        return jsonify({
            'error': 'Internal server error',
            'timestamp': datetime.utcnow().isoformat()
        }), 500

    @app.errorhandler(Exception)
    def handle_exception(error):
        app.logger.error(f"Unhandled exception: {str(error)}")
        return jsonify({
            'error': 'Internal server error',
            'timestamp': datetime.utcnow().isoformat()
        }), 500