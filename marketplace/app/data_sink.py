"""This module contains all functionality regarding data sink apps..

.. currentmodule:: marketplace.app.data_sink_app
.. moduleauthor:: Pablo de Andres, Pranjali Singh (Fraunhofer IWM)
"""
from ..models import DatasetCreateResponse, DatasetId, DatasetModel
from .base import _AppBase
from .utils import check_capability_availability


class DataSinkApp(_AppBase):
    @check_capability_availability
    def create_dataset(self, dataset: DatasetModel) -> DatasetId:
        """Create a new dataset.

        :param dataset: the dataset to create
        :return: the created dataset
        """
        response = self.client.post("datasets", json=dataset)
        response.raise_for_status()
        return DatasetCreateResponse(**response.json()).id
