from .object_storage import MarketPlaceObjectStorageApp
from .system import MarketPlaceSystemApp
from .transformation import MarketPlaceTransformationApp


class MarketPlaceApp(
    MarketPlaceObjectStorageApp, MarketPlaceTransformationApp, MarketPlaceSystemApp
):
    pass
