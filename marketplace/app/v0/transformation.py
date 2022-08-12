import json

import marketplace_standard_app_api.models.transformation as TransformationModel

from ..utils import check_capability_availability
from .base import _MarketPlaceAppBase


class MarketPlaceTransformationApp(_MarketPlaceAppBase):
    @check_capability_availability
    def get_transformation_list(
        self, limit: int = 100, offset: int = 0
    ) -> TransformationModel.TransformationListResponse:
        params = {"limit": limit, "offset": offset}
        return TransformationModel.TransformationListResponse.parse_obj(
            json.loads(self._client.get("getTransformationList", params=params))
        )

    @check_capability_availability
    def new_transformation(
        self, transformation: TransformationModel.NewTransformationModel
    ) -> TransformationModel.TransformationCreateResponse:
        return TransformationModel.TransformationCreateResponse.parse_obj(
            json.loads(self._client.post("newTransformation", json=transformation))
        )

    @check_capability_availability
    def get_transformation(
        self, transformation_id: TransformationModel.TransformationId
    ) -> TransformationModel.TransformationModel:
        params = {"transformation_id": transformation_id}
        return TransformationModel.TransformationModel.parse_obj(
            json.loads(self._client.get("getTransformation", params=params))
        )

    @check_capability_availability
    def delete_transformation(
        self, transformation_id: TransformationModel.TransformationId
    ):
        params = {"transformation_id": transformation_id}
        return self._client.delete("deleteTransformation", params=params)

    # TODO: check request type (in standard app api its patch)
    @check_capability_availability
    def update_transformation(
        self,
        transformation_id: TransformationModel.TransformationId,
        update: TransformationModel.TransformationUpdateModel,
    ) -> TransformationModel.TransformationUpdateResponse:
        params = {"transformation_id": transformation_id}
        return TransformationModel.TransformationUpdateResponse.parse_obj(
            json.loads(
                self._client.put("updateTransformation", params=params, json=update)
            )
        )

    @check_capability_availability
    def get_transformation_state(
        self, transformation_id: TransformationModel.TransformationId
    ) -> TransformationModel.TransformationStateResponse:
        params = {"transformation_id": transformation_id}
        return TransformationModel.TransformationStateResponse.parse_obj(
            json.loads(self._client.get("getTransformationState", params=params))
        )
