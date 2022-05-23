"""This module contains all functionality regarding data source apps..

.. currentmodule:: marketplace.app.data_source_app
.. moduleauthor:: Pablo de Andres, Pranjali Singh (Fraunhofer IWM)
"""

from ..models import DatasetId, DatasetModel
from .base import _AppBase
from .utils import check_capability_availability


class DataSourceApp(_AppBase):
    @check_capability_availability
    def get_dataset(self, dataset_id: DatasetId) -> DatasetModel:
        """Retrive an existing dataset.

        :param dataset_id: the id of the dataset
        :return: the dataset
        """
        response = self.client.get(f"datasets/{dataset_id}")
        response.raise_for_status()
        return DatasetModel(**response.json())
