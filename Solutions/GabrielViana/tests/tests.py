import pytest
from tests.test_utils import TestUtils
from io import BytesIO



from app import create_app

@pytest.fixture
def app():
    """Create a Flask app instance for testing."""
    app = create_app('testing')
    yield app
    
    
def client(app):
    """Create a test client for the Flask app."""
    return app.test_client()


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/health')
    assert response.status_code == 200
    
def test_upload_png(client):
    random_images = TestUtils.generate_random_images()
    
    data = {
        'file': (BytesIO(random_images[0]), 'test_image.png')
    }

    response = client.post(
        "/upload",
        content_type='multipart/form-data',
        data=data
    )


    assert response.status_code == 200
    
def test_process(client):
    """Test the process endpoint."""
    response = client.get('/process')
    assert response.status_code == 200

    