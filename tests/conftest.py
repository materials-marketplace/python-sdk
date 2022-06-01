#!/usr/bin/env python

""".. currentmodule:: conftest.

.. moduleauthor:: Carl Simon Adorf <simon.adorf@epfl.ch>

Provide fixtures for all tests.
"""

import pytest


@pytest.fixture
def environment(monkeypatch):
    # Full tests will eventually require a local development deployment of the
    # MarketPlace platform.
    monkeypatch.setenv("MP_HOST", "https://lvh.me")
    # For now, we are not providing a mock marketplace, all tests will
    # therefore be runnable with empty tokens.
    monkeypatch.setenv("MP_ACCESS_TOKEN", "")
    monkeypatch.setenv("MP_REFRESH_TOKEN", "")
