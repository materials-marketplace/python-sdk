from marketplace_standard_app_api.models.object_storage import CollectionListResponse

from .base import _MarketPlaceAppBase


class MarketPlaceObjectStorageApp(_MarketPlaceAppBase):
    def list_collections(
        self, limit: int = 100, offset: int = 0
    ) -> CollectionListResponse:
        return CollectionListResponse(**self._client.get("/data").json())
