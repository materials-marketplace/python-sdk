import json

import marketplace_standard_app_api.models.transformation as TransformationModel

from ..utils import check_capability_availability
from .base import _MarketPlaceAppBase


class MarketPlaceObjectStorageApp(_MarketPlaceAppBase):
    # TODO: figure out if this is create_transformation or new_transformation
    @check_capability_availability
    def new_transformation(
        self, transformation: TransformationModel.NewTransformationModel
    ) -> TransformationModel.TransformationCreateResponse:
        return TransformationModel.TransformationCreateResponse.parse_obj(
            json.loads(self._client.post("/transformations", json=transformation))
        )

    @check_capability_availability
    def get_transformation(
        self, transformation_id: TransformationModel.TransformationId
    ) -> TransformationModel.TransformationModel:
        return TransformationModel.TransformationModel.parse_obj(
            json.loads(self._client.get(f"/{transformation_id}"))
        )

    @check_capability_availability
    def delete_transformation(
        self, transformation_id: TransformationModel.TransformationId
    ):
        return self._client.delete(f"/{transformation_id}")

    # TODO: check request type (in standard app api its patch)
    @check_capability_availability
    def update_transformation(
        self,
        transformation_id: TransformationModel.TransformationId,
        update: TransformationModel.TransformationUpdateModel,
    ) -> TransformationModel.TransformationUpdateResponse:
        return TransformationModel.TransformationUpdateResponse.parse_obj(
            json.loads(self._client.put(f"/{transformation_id}", json=update))
        )

    @check_capability_availability
    def get_transformation_state(
        self, transformation_id: TransformationModel.TransformationId
    ) -> TransformationModel.TransformationStateResponse:
        return TransformationModel.TransformationStateResponse.parse_obj(
            json.loads(self._client.get(f"/{transformation_id}/state"))
        )

    # TODO: operation id is getTransformationList but in standard api function name is list_transformation
    # figure out correct name
    @check_capability_availability
    def get_transformation_list(
        self, limit: int = 100, offset: int = 0
    ) -> TransformationModel.TransformationListResponse:
        return TransformationModel.TransformationListResponse.parse_obj(
            json.loads(self._client.get("/transformations"))
        )
