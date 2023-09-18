"""This module contains MarketPlaceClient to enable interaction with the MarketPlace.

.. currentmodule:: marketplace.core
.. moduleauthor:: Carl Simon Adorf <simon.adorf@epfl.ch>,
                  Pablo de Andres <pablo.de.andres@iwm.fraunhofer.de>
"""

import os
from functools import wraps
from urllib.parse import urljoin

import requests
from keycloak import KeycloakOpenID
from requests import Response

from .version import __version__

MP_DEFAULT_HOST = "https://materials-marketplace.eu/"


def configure_token(func):
    @wraps(func)
    def func_(self, *arg, **kwargs):
        r = func(self, *arg, **kwargs)
        if r.status_code == 401:
            token = configure()
            if token is None:
                raise (
                    "Authentication failure. Please provide valid MP_ACCESS_TOKEN or keycloak credentials."
                )
            os.environ["MP_ACCESS_TOKEN"] = token
            self.access_token = token

        r = func(self, *arg, **kwargs)
        if r.status_code > 400:
            raise Exception("Server returned with an Exception. Details: ", r.text)
        return r

    return func_


def configure():
    # Configure client
    server_url = os.environ.get("KEYCLOAK_SERVER_URL")
    client_id = os.environ.get("KEYCLOAK_CLIENT_ID")
    realm_name = os.environ.get("KEYCLOAK_REALM_NAME")
    client_key = os.environ.get("KEYCLOAK_CLIENT_SECRET_KEY")
    user = os.environ.get("MARKETPLACE_USERNAME")
    passwd = os.environ.get("MARKETPLACE_PASSWORD")
    keycloak_openid = KeycloakOpenID(
        server_url=server_url,
        client_id=client_id,
        realm_name=realm_name,
        client_secret_key=client_key,
    )
    try:
        token = keycloak_openid.token(user, passwd)
        token = token["access_token"]
        return token
    except Exception:
        return None


class MarketPlaceClient:
    """Interact with the MarketPlace platform."""

    def __init__(self, marketplace_host_url=None, access_token=None):
        marketplace_host_url = marketplace_host_url or os.environ.get(
            "MP_HOST",
            MP_DEFAULT_HOST,
        )
        access_token = access_token or os.environ.get("MP_ACCESS_TOKEN")

        self.marketplace_host_url = marketplace_host_url
        self.access_token = access_token

    @property
    def default_headers(self):
        """Generate default headers to be used with every request."""
        return {
            "User-Agent": f"MarketPlace Python SDK {__version__}",
            "Authorization": f"Bearer {self.access_token}",
        }

    @property
    def url_userinfo(self):
        return (
            f"{self.marketplace_host_url}"
            "auth/realms/marketplace/protocol/openid-connect/userinfo"
        )

    @property
    def userinfo(self):
        userinfo = self.get(self.url_userinfo)
        userinfo.raise_for_status()
        return userinfo.json()

    def _request(self, op, path, **kwargs) -> Response:
        kwargs.setdefault("headers", {}).update(self.default_headers)
        full_url = urljoin(self.marketplace_host_url, path)
        return op(url=full_url, **kwargs)

    @configure_token
    def get(self, path: str, **kwargs):
        return self._request(requests.get, path, **kwargs)

    @configure_token
    def post(self, path: str, **kwargs):
        return self._request(requests.post, path, **kwargs)

    @configure_token
    def put(self, path: str, **kwargs):
        return self._request(requests.put, path, **kwargs)

    @configure_token
    def delete(self, path: str, **kwargs):
        return self._request(requests.delete, path, **kwargs)

    @configure_token
    def head(self, path: str, **kwargs):
        return self._request(requests.head, path, **kwargs)

    @configure_token
    def patch(self, path: str, **kwargs):
        return self._request(requests.patch, path, **kwargs)
