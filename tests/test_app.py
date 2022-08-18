import pytest

from marketplace.app import MarketPlaceApp


@pytest.fixture
def app():
    return MarketPlaceApp()


def test_app(app):
    pass
