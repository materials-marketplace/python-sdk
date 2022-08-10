import json

from fastapi.responses import HTMLResponse
from marketplace_standard_app_api.models.system import GlobalSearchResponse

from ..utils import check_capability_availability


class _MarketPlaceAppBase:
    def __init__(self, client, app_id, capabilities):
        self._client = client
        self.app_id = app_id

        # self._capabilities = self._client.get_app_capabilities(self.app_id)  # TODO
        self._capabilities = capabilities  # FOR DEBUGGING

    # TODO: operationId is 'frontend' but function name is 'frontpage'
    # figure out the correct one
    @check_capability_availability
    def frontend(self) -> HTMLResponse:
        return self._client.get("/")

    @check_capability_availability
    def heartbeat(self) -> HTMLResponse:
        return self._client.get("/health")

    # TODO: is this correct way to pass quey parameters?
    @check_capability_availability
    def global_search(
        self, q: str, limit: int = 100, offset: int = 0
    ) -> GlobalSearchResponse:
        return GlobalSearchResponse.parse_obj(
            json.loads(self._client.get("/globalSearch", {"q": q}))
        )
