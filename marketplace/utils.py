"""General utilities for interacting with a MarketPlace instance."""

import os
from keycloak import KeycloakOpenID
from marketplace.client import MP_DEFAULT_HOST


def get_access_token(
    marketplace_host_url: str = None,
    client_id: str = "python_sdk",
    username: str = "",
    password: str = "",
) -> str:
    marketplace_host_url = marketplace_host_url or os.environ.get(
        "MP_HOST",
        MP_DEFAULT_HOST,
    )
    username = username or os.environ.get("MP_USERNAME")
    password = password or os.environ.get("MP_PASSWORD")

    if not (username and password):
        raise ValueError("username and/or password not defined.")

    keycloak_openid = KeycloakOpenID(server_url=marketplace_host_url,
                                    realm_name="marketplace",
                                    client_id=client_id,
                                    client_secret_key="secret")
    return keycloak_openid.token(username, password)
