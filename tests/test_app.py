import pytest

from marketplace.app import get_app


@pytest.fixture
def app():
    return get_app("test-app")


def test_app_v0(app):
    assert "heartbeat" in app.capabilities
    response = app.heartbeat()
    assert response.ok
    assert "frontend" in app.capabilities
    response = app.frontend()
    assert response.ok
    assert "Hello app!" in response.text
