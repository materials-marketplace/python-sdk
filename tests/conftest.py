#!/usr/bin/env python

""".. currentmodule:: conftest.

.. moduleauthor:: Carl Simon Adorf <simon.adorf@epfl.ch>

Provide fixtures for all tests.
"""

import re
from urllib.parse import urljoin

import pytest

from marketplace.client import MP_DEFAULT_HOST


@pytest.fixture
def _app_service_response():
    return {
        "api_version": "0.3.0",
        "capabilities": [
            {"name": "frontend"},
            {"name": "getObject"},
            {"name": "heartbeat"},
        ],
    }


@pytest.fixture
def _app_service(requests_mock, _app_service_response):
    application_service = re.compile(f"{MP_DEFAULT_HOST}api/applications/.*")

    requests_mock.get(application_service, json=_app_service_response)


@pytest.fixture
def _proxy_service(requests_mock):
    proxy_path = "api/applications/proxy"
    requests_mock.get(
        re.compile(urljoin(MP_DEFAULT_HOST, proxy_path) + r"/.*/frontend"),
        text="<html><body>Hello app!</body></html>",
    )
    requests_mock.get(
        re.compile(urljoin(MP_DEFAULT_HOST, proxy_path) + r"/.*/heartbeat"), text="OK"
    )
    # mocking the older version
    requests_mock.get(
        re.compile(urljoin(MP_DEFAULT_HOST, "mp-api/proxy") + r"/.*/heartbeat"),
        text="OK",
    )


@pytest.fixture(autouse=True)
def environment(monkeypatch, _app_service, _proxy_service):
    monkeypatch.setenv("MP_ACCESS_TOKEN", "")
    monkeypatch.setenv("MP_REFRESH_TOKEN", "")
