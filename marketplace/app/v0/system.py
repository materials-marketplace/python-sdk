from typing import Optional

from fastapi.responses import JSONResponse, Response

from ..utils import check_capability_availability


@check_capability_availability
def get_logs(self, id: Optional[str], limit: int = 100, offset: int = 0) -> Response:
    return self._client.get(
        self._proxy_path("getLogs"),
        params={"id": id, "limit": limit, "offset": offset},
    ).content


@check_capability_availability
def get_info(self, config: dict = None) -> JSONResponse:
    params = {}
    if config is not None:
        params.update(config)
    return self._client.get(self._proxy_path("getInfo"), params=params).json()
