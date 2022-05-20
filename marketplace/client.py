"""This module contains MarketPlaceClient to enable interaction with the MarketPlace.

.. currentmodule:: marketplace.core
.. moduleauthor:: Carl Simon Adorf <simon.adorf@epfl.ch>,
                  Pablo de Andres <pablo.de.andres@iwm.fraunhofer.de>
"""

import os
from urllib.parse import urljoin

import requests

from .version import __version__


class Client:
    """Interact with the MarketPlace platform."""

    def __init__(self, marketplace_host_url=None, access_token=None):
        marketplace_host_url = marketplace_host_url or os.environ.get(
            "MP_HOST", "https://www.materials-marketplace.eu/"
        )
        access_token = access_token or os.environ["MP_ACCESS_TOKEN"]
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": f"MarketPlaceClient/{__version__}",
                "Authorization": f"Bearer {access_token}",
            }
        )

        self.marketplace_host_url = marketplace_host_url
        self.access_token = access_token

    def get(self, url: str, **kwargs):
        return self.session.get(urljoin(self.marketplace_host_url, url), **kwargs)

    def post(self, url: str, **kwargs):
        return self.session.post(urljoin(self.marketplace_host_url, url), **kwargs)

    def put(self, url: str, **kwargs):
        return self.session.put(urljoin(self.marketplace_host_url, url), **kwargs)

    def patch(self, url: str, **kwargs):
        return self.session.patch(urljoin(self.marketplace_host_url, url), **kwargs)

    def delete(self, url: str, **kwargs):
        return self.session.delete(urljoin(self.marketplace_host_url, url), **kwargs)

    def userinfo(self, **kwargs):
        response = self.get(
            "/auth/realms/marketplace/protocol/openid-connect/userinfo", **kwargs
        )
        response.raise_for_status()
        return response.json()
