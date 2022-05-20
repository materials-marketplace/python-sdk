from urllib.parse import urljoin
from uuid import UUID

from ..applicaton_proxy import ApplicationProxy
from ..client import Client
from ..models import ApplicationId


class _AppBase:
    """Interact with a MarketPlace application."""

    def __init__(self, application_id: ApplicationId | str, **kwargs):
        self.client = Client(**kwargs)
        self.application_id = (
            ApplicationId(UUID(application_id))
            if isinstance(application_id, str)
            else application_id
        )
        self.application_proxy = ApplicationProxy(self.client, self.application_id)

        self._capabilities = self._determine_capabilities

    def _determine_capabilities(self) -> set[str]:
        """Determine the capabilities of the application."""
        app_service_path = f"application-service/applications/{self.application_id}"
        response = self.client.get(urljoin(app_service_path, "capabilities"))
        response.raise_for_status()
        return set(response.json()["capabilities"])

    def healthy(self) -> bool:
        """Check whether the application is running and available."""
        response = self.client.get("health")
        if response.status_code == 200:
            return True
        elif response.status_code == 503:
            return False
        response.raise_for_status()
        return False
