#!/usr/bin/env python
# -*- coding: utf-8 -*-

""".. currentmodule:: test_core.

.. moduleauthor:: Carl Simon Adorf <simon.adorf@epfl.ch>
"""
import pytest

from marketplace.client import Client


@pytest.fixture
def client(environment):
    client = Client()
    yield client


def test_constructor(client):
    pass


def test_default_headers(client):
    headers = client.default_headers
    assert len(headers) >= 2
    for key in ("User-Agent", "Authorization"):
        assert key in headers
