from requests import Response

from .client import Client
from .models import ApplicationId


class ApplicationProxy:
    def __init__(self, client: Client, application_id: ApplicationId):
        self.client = client
        self.application_id = application_id
        self._proxy_url = f"mp-api/proxy/{application_id}/"

    def get(self, url: str, **kwargs) -> Response:
        """Get a resource from the application."""
        return self.client.get(f"{self._proxy_url}/{url}", **kwargs)

    def post(self, url: str, **kwargs) -> Response:
        """Post a resource to the application."""
        return self.client.post(f"{self._proxy_url}/{url}", **kwargs)

    def put(self, url: str, **kwargs) -> Response:
        """Put a resource to the application."""
        return self.client.put(f"{self._proxy_url}/{url}", **kwargs)

    def patch(self, url: str, **kwargs) -> Response:
        """Patch a resource to the application."""
        return self.client.patch(f"{self._proxy_url}/{url}", **kwargs)

    def delete(self, url: str, **kwargs) -> Response:
        """Delete a resource from the application."""
        return self.client.delete(f"{self._proxy_url}/{url}", **kwargs)
