"""This module contains all functionality regarding transformation apps..

.. currentmodule:: marketplace.app.transformation_app
.. moduleauthor:: Pablo de Andres, Pranjali Singh (Fraunhofer IWM)
"""

from ..models import (
    NewTransformationModel,
    TransformationCreateResponse,
    TransformationId,
    TransformationModel,
    TransformationStatus,
    TransformationStatusResponse,
    TransformationUpdateModel,
    TransformationUpdateResponse,
)
from .base import _AppBase
from .utils import check_capability_availability


class TransformationApp(_AppBase):
    @check_capability_availability
    def create_transformation(
        self, transformation: NewTransformationModel
    ) -> TransformationId:
        """Create a new transformation.

        :param transformation: the transformation to create
        :return: the created transformation
        """
        response = self.client.post("transformations", json=transformation)
        response.raise_for_status()
        return TransformationCreateResponse(**response.json()).id

    @check_capability_availability
    def get_transformation(
        self, transformation_id: TransformationId
    ) -> TransformationModel:
        """Get an existing transformation.

        Note that the status field maybe None, because determining the status
        could be a costly operation. Use the get_transformation_status method to
        get the status.

        :param transformation_id: the id of the transformation
        :return: the transformation
        """
        response = self.client.get(f"transformations/{transformation_id}")
        response.raise_for_status()
        return TransformationModel(**response.json())

    @check_capability_availability
    def delete_transformation(self, transformation_id: TransformationId):
        """Delete an existing transformation.

        :param transformation_id: the id of the transformation
        """
        response = self.client.delete(f"transformations/{transformation_id}")
        response.raise_for_status()
        if not response.status_code == 204:
            raise RuntimeError(
                f"Transformation {transformation_id} could not be deleted."
            )

    @check_capability_availability
    def _update_transformation(
        self, transformation_id: TransformationId, update: TransformationUpdateResponse
    ):
        """Update the status of an existing transformation.

        :param transformation_id: the id of the transformation
        :param transformation: the transformation to update
        """
        response = self.client.patch(
            f"transformations/{transformation_id}", json=update
        )
        if response.status_code == 409:
            raise RuntimeError(
                "The requests status is no longer available. "
                "Typically indicates that the transformation has already entered a terminal state."
            )
        response.raise_for_status()
        return TransformationUpdateResponse(**response.json())

    def start_transformation(self, transformation_id: TransformationId):
        """Start an existing transformation.

        :param transformation_id: the id of the transformation
        """
        self._update_transformation(
            transformation_id,
            TransformationUpdateModel(status=TransformationStatus.RUNNING),
        )

    def stop_transformation(self, transformation_id: TransformationId):
        """Stop an existing transformation.

        :param transformation_id: the id of the transformation
        """
        self._update_transformation(
            transformation_id,
            TransformationUpdateModel(status=TransformationStatus.STOPPED),
        )

    @check_capability_availability
    def get_transformation_status(
        self, transformation_id: TransformationId
    ) -> TransformationStatus:
        """Get the status of a transformation from the MarketPlace.

        :param transformation_id: the id of the transformation
        :return: the transformation
        """
        response = self.client.get(f"transformations/{transformation_id}/status")
        response.raise_for_status()
        return TransformationStatusResponse(**response.json()).status

    @check_capability_availability
    def list_transformations(
        self, limit: int = 100, offset: int = 0
    ) -> list[TransformationModel]:
        """List all transformations in the MarketPlace.

        :param limit: the maximum number of transformations to return
        :param offset: the offset to start the list
        :return: the list of transformations
        """
        response = self.client.get(f"transformations?limit={limit}&offset={offset}")
        response.raise_for_status()
        return [TransformationModel(**t) for t in response.json()["items"]]
