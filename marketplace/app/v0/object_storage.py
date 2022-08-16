import json
import re

import marketplace_standard_app_api.models.object_storage as object_storage
from fastapi import UploadFile

from ..utils import check_capability_availability
from .base import _MarketPlaceAppBase


class MarketPlaceObjectStorageApp(_MarketPlaceAppBase):
    def __encode_metadata(self, metadata: dict = None) -> dict:
        return {
            f"X-Object-Meta-{name}": json.dumps(value)
            for name, value in metadata.items()
        }

    def __decode_metadata(self, headers: dict = None) -> dict:
        return {
            re.sub(r"^X-Object-Meta-", "", name): json.loads(value)
            for name, value in headers.items()
            if str(name).startswith("X-Object-Meta-")
        }

    @check_capability_availability
    def list_collections(
        self, limit: int = 100, offset: int = 0
    ) -> object_storage.CollectionListResponse:
        return object_storage.CollectionListResponse(
            **self._client.get(
                "listCollections", params={"limit": limit, "offset": offset}
            ).json()
        )

    @check_capability_availability
    def list_datasets(
        self,
        collection_name: object_storage.CollectionName,
        limit: int = 100,
        offset: int = 0,
    ) -> object_storage.DatasetListResponse:
        return object_storage.DatasetListResponse(
            **self._client.get(
                "listDatasets",
                params={
                    "collection_name": collection_name,
                    "limit": limit,
                    "offset": offset,
                },
            ).json()
        )

    @check_capability_availability
    def create_or_update_collection(
        self,
        metadata: dict = None,
        collection_name: object_storage.CollectionName = None,
    ):
        return self._client.put(
            "createOrUpdateCollection",
            params={"collection_name": collection_name} if collection_name else {},
            headers=self.__encode_metadata(metadata),
        ).json()

    @check_capability_availability
    def delete_collection(self, collection_name: object_storage.CollectionName):
        return self._client.delete(
            "deleteCollection", params={"collection_name": collection_name}
        ).json()

    # NOTE: change to GET for the meeting if proxy doesn't support HEAD requests
    @check_capability_availability
    def get_collection_metadata(self, collection_name: object_storage.CollectionName):
        response_headers: dict = self._client.head(
            "getCollectionMetadata", params={"collection_name": collection_name}
        ).headers
        return json.dumps(self.__decode_metadata(headers=response_headers))

    @check_capability_availability
    def create_collection(
        self,
        collection_name: object_storage.CollectionName = None,
        metadata: dict = None,
    ):
        return self._client.put(
            "createCollection",
            params={"collection_name": collection_name} if collection_name else {},
            headers=self.__encode_metadata(metadata),
        ).json()

    @check_capability_availability
    def create_dataset(
        self,
        collection_name: object_storage.CollectionName,
        dataset_name: object_storage.DatasetName = None,
        metadata: dict = None,
        file: UploadFile = None,
    ) -> object_storage.DatasetCreateResponse:
        params = {"collection_name": collection_name}
        if dataset_name:
            params.update({"dataset_name": dataset_name})
        return object_storage.DatasetCreateResponse.parse_obj(
            json.loads(self._client.put(
                "createDataset",
                params=params,
                headers=self.__encode_metadata(metadata),
                data=file.file,
            ))
        )

    # TODO: POST or PUT. as headers or in the body?
    @check_capability_availability
    def create_dataset_metadata(
        self,
        collection_name: object_storage.CollectionName,
        dataset_name: object_storage.DatasetName = None,
        metadata: dict = None,
    ):
        params = {"collection_name": collection_name}
        if dataset_name:
            params.update({"dataset_name": dataset_name})
        return self._client.post(
            "createDatasetMetadata",
            params=params,
            headers=self.__encode_metadata(metadata),
        )

    @check_capability_availability
    def get_dataset(
        self,
        collection_name: object_storage.CollectionName,
        dataset_name: object_storage.DatasetName,
    ):
        return self._client.get(
            "getDataset",
            params={"collection_name": collection_name, "dataset_name": dataset_name},
        ).json()

    def create_or_replace_dataset(
        self,
        collection_name: object_storage.CollectionName,
        dataset_name: object_storage.DatasetName = None,
        metadata: dict = None,
        file: UploadFile = None,
    ) -> object_storage.DatasetCreateResponse:
        params = {"collection_name": collection_name}
        if dataset_name:
            params.update({"dataset_name": dataset_name})
        return object_storage.DatasetCreateResponse(
            **self._client.put(
                "createOrReplaceDataset",
                params=params,
                headers=self.__encode_metadata(metadata),
                data=file.file,
            )
        )

    # TODO: in header or in request body?
    @check_capability_availability
    def create_or_replace_dataset_metadata(
        self,
        collection_name: object_storage.CollectionName,
        dataset_name: object_storage.DatasetName,
        metadata: dict = None,
    ):
        return self._client.put(
            "createOrReplaceDatasetMetadata",
            params={"collection_name": collection_name, "dataset_name": dataset_name},
            headers=self.__encode_metadata(metadata),
        )

    @check_capability_availability
    def delete_dataset(
        self,
        collection_name: object_storage.CollectionName,
        dataset_name: object_storage.DatasetName,
    ):
        return self._client.delete(
            "deleteDataset",
            params={"collection_name": collection_name, "dataset_name": dataset_name},
        ).json()

    # NOTE: change to GET for the meeting if proxy doesn't support HEAD requests
    @check_capability_availability
    def get_dataset_metadata(
        self,
        collection_name: object_storage.CollectionName,
        dataset_name: object_storage.DatasetName,
    ):
        response_headers: dict = self._client.head(
            "getDatasetMetadata",
            params={"collection_name": collection_name, "dataset_name": dataset_name},
        ).headers
        return json.dumps(self.__decode_metadata(headers=response_headers))

    @check_capability_availability
    def list_semantic_mappings(
        self, limit: int = 100, offset: int = 0
    ) -> object_storage.SemanticMappingListResponse:
        return object_storage.SemanticMappingListResponse(
            **self._client.get(
                "listSemanticMappings", params={"limit": limit, "offset": offset}
            ).json()
        )

    @check_capability_availability
    def get_semantic_mapping(
        self, semantic_mapping_id: str
    ) -> object_storage.SemanticMappingModel:
        return object_storage.SemanticMappingModel.parse_obj(
            json.loads(
                self._client.get(
                    "getSemanticMapping",
                    params={"semantic_mapping_id": semantic_mapping_id},
                )
            )
        )
