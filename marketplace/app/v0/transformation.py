import marketplace_standard_app_api.models.transformation as transformation

from ..utils import check_capability_availability
from .base import _MarketPlaceAppBase


class MarketPlaceTransformationApp(_MarketPlaceAppBase):
    @check_capability_availability
    def get_transformation_list(
        self, limit: int = 100, offset: int = 0
    ) -> transformation.TransformationListResponse:
        return transformation.TransformationListResponse.parse_obj(
            self._client.get(
                self._proxy_path("getTransformationList"),
                params={"limit": limit, "offset": offset},
            ).json()
        )

    @check_capability_availability
    def new_transformation(
        self,
        new_transformation: transformation.NewTransformationModel,
        config: dict = None,
    ) -> transformation.TransformationCreateResponse:
        """
        Creates a new transformation.

        Args:
        - new_transformation (NewTransformationModel): A dictionary representing
            parameters to create a new transformation.
        - config (dict): A dictionary representing query parameters.
            Any key-value passed inside this dictionary are sent as query parameters
            to the application.

        Retruns:
            TransformationCreateResponse: A dictionary containing id of the
            created transformation.
        """
        params = {}
        # send additional key value as query parameters if some app needs it
        if config is not None:
            params.update(config)
        return transformation.TransformationCreateResponse.parse_obj(
            self._client.post(
                self._proxy_path("newTransformation"),
                json=new_transformation,
                params=params,
            ).json()
        )

    @check_capability_availability
    def get_transformation(
        self, transformation_id: transformation.TransformationId
    ) -> transformation.TransformationModel:
        return transformation.TransformationModel.parse_obj(
            self._client.get(
                self._proxy_path("getTransformation"),
                params={"transformation_id": transformation_id},
            ).json()
        )

    @check_capability_availability
    def delete_transformation(self, transformation_id: transformation.TransformationId):
        self._client.delete(
            self._proxy_path("deleteTransformation"),
            params={"transformation_id": transformation_id},
        )

    @check_capability_availability("update_transformation")
    def _update_transformation(
        self,
        transformation_id: transformation.TransformationId,
        update: transformation.TransformationUpdateModel,
    ) -> transformation.TransformationUpdateResponse:
        return transformation.TransformationUpdateResponse.parse_obj(
            self._client.patch(
                self._proxy_path("updateTransformation"),
                params={"transformation_id": transformation_id},
                json=update.dict(),
            ).json()
        )

    def start_transformation(
        self, transformation_id: transformation.TransformationId
    ) -> transformation.TransformationStateResponse:
        update: transformation.TransformationUpdateModel = (
            transformation.TransformationUpdateModel(
                state=transformation.TransformationState.RUNNING
            )
        )
        update_response: transformation.TransformationUpdateResponse = (
            self._update_transformation(
                transformation_id=transformation_id, update=update
            )
        )
        return transformation.TransformationStateResponse.parse_obj(
            update_response.dict()
        )

    def stop_transformation(
        self, transformation_id: transformation.TransformationId
    ) -> transformation.TransformationStateResponse:
        update: transformation.TransformationUpdateModel = (
            transformation.TransformationUpdateModel(
                state=transformation.TransformationState.STOPPED
            )
        )
        update_response: transformation.TransformationUpdateResponse = (
            self._update_transformation(
                transformation_id=transformation_id, update=update
            )
        )
        return transformation.TransformationStateResponse.parse_obj(
            update_response.dict()
        )

    @check_capability_availability
    def get_transformation_state(
        self, transformation_id: transformation.TransformationId
    ) -> transformation.TransformationState:
        return transformation.TransformationStateResponse.parse_obj(
            self._client.get(
                self._proxy_path("getTransformationState"),
                params={"transformation_id": transformation_id},
            ).json()
        ).state
