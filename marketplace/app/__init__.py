"""Module for handling the different types of MarketPlace apps and their
capabilities.
.. currentmodule:: marketplace.app
.. moduleauthor:: Pablo de Andres, Pranjali Singh (Fraunhofer IWM)
"""
from .data_sink import DataSinkApp
from .data_source import DataSourceApp
from .transformation import TransformationApp


class MarketPlaceApp(DataSinkApp, DataSourceApp, TransformationApp):
    """MarketPlace app with all capabilities."""


__all__ = [
    "DataSinkApp",
    "DataSourceApp",
    "MarketPlaceApp",
    "TransformationApp",
]
