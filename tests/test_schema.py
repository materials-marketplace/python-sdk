import json
from pathlib import Path

import pytest

from marketplace.api import api


@pytest.fixture
def marketplace_openapi_specification_file_path():
    return Path("openapi.json")


@pytest.fixture
def marketplace_openapi_specification_file():
    return json.loads(Path("openapi.json").read_text())


@pytest.fixture
def marketplace_api():
    return api


@pytest.fixture
def marketplace_openapi():
    return api.openapi()


def test_marketplace_openapi_specification_is_present(
    marketplace_openapi_specification_file_path,
):
    return marketplace_openapi_specification_file_path.exists()


def test_marketplace_openapi_specification_file_in_sync(
    marketplace_openapi_specification_file,
    marketplace_openapi,
):
    assert marketplace_openapi_specification_file == marketplace_openapi
