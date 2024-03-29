#!/usr/bin/env python

""".. currentmodule:: test_core.

.. moduleauthor:: Carl Simon Adorf <simon.adorf@epfl.ch>
"""
import pytest

from marketplace.client import MarketPlaceClient


@pytest.fixture
def marketplace(environment):
    instance = MarketPlaceClient()
    yield instance


def test_constructor(marketplace):
    pass


def test_default_headers(marketplace):
    headers = marketplace.default_headers
    assert len(headers) >= 2
    for key in ("User-Agent", "Authorization"):
        assert key in headers
