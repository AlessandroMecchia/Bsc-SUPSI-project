import pytest
from web_service import create_app

@pytest.fixture
def client():
    app = create_app()
    return app.test_client()


class TestActivities:
    pass
    # GET /activities