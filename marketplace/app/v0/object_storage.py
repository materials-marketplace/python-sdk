import json

import marketplace_standard_app_api.models.object_storage as ObjectStorageModel
from fastapi import Request, UploadFile

from ..utils import check_capability_availability
from .base import _MarketPlaceAppBase


class MarketPlaceObjectStorageApp(_MarketPlaceAppBase):
    @check_capability_availability
    def list_collections(
        self, limit: int = 100, offset: int = 0
    ) -> ObjectStorageModel.CollectionListResponse:
        params = {"limit": limit, "offset": offset}
        return ObjectStorageModel.CollectionListResponse(
            **self._client.get("listCollections", params).json()
        )

    @check_capability_availability
    def list_datasets(
        self,
        collection_name: ObjectStorageModel.CollectionName,
        limit: int = 100,
        offset: int = 0,
    ) -> ObjectStorageModel.DatasetListResponse:
        params = {"collection_name": collection_name, "limit": limit, "offset": offset}
        return ObjectStorageModel.DatasetListResponse(
            **self._client.get("listDatasets", params=params).json()
        )

    # TODO: check this implementation
    @check_capability_availability
    def create_or_update_collection(
        self,
        request: Request,
        collection_name: ObjectStorageModel.CollectionName = None,
    ):
        params = {}
        if collection_name:
            params = {"collection_name": collection_name}
        return self._client.put(
            "createOrUpdateCollection",
            params=params,
            headers=request.headers,
            json=request.json(),
        ).json()

    @check_capability_availability
    def delete_collection(self, collection_name: ObjectStorageModel.CollectionName):
        params = {"collection_name": collection_name}
        return self._client.delete("deleteCollection", params=params).json()

    # TODO: check implementation
    @check_capability_availability
    def get_collection_metadata(
        self, collection_name: ObjectStorageModel.CollectionName
    ):
        params = {"collection_name": collection_name}
        response_headers: dict = self._client.get(
            "getCollectionMetadata", params=params
        ).headers
        return json.dumps(
            dict(
                filter(
                    lambda val: str(val[0]).startswith("X-Object-Meta"),
                    response_headers.items(),
                )
            )
        )

    # TODO: check implementation
    @check_capability_availability
    def create_collection(
        self,
        request: Request,
        collection_name: ObjectStorageModel.CollectionName = None,
    ):
        params = {}
        if collection_name:
            params = {"collection_name": collection_name}
        return self._client.put(
            "createCollection",
            params=params,
            headers=request.headers,
            json=request.json(),
        ).json()

    # TODO: check implementation
    @check_capability_availability
    def create_dataset(
        self,
        request: Request,
        file: UploadFile,
        collection_name: ObjectStorageModel.CollectionName,
        dataset_name: ObjectStorageModel.DatasetName = None,
    ) -> ObjectStorageModel.DatasetCreateResponse:
        params = {"collection_name": collection_name}
        if dataset_name:
            params.update({"dataset_name": dataset_name})
        return ObjectStorageModel.DatasetCreateResponse(
            **self._client.put(
                "createDataset", params=params, headers=request.headers, data=file.file
            )
        )

    # TODO: metadata header?
    def create_dataset_metadata(
        self,
        collection_name: ObjectStorageModel.CollectionName,
        dataset_name: ObjectStorageModel.DatasetName = None,
        payload=None,
    ):
        params = {"collection_name": collection_name}
        if dataset_name:
            params.update({"dataset_name": dataset_name})
        return self._client.post("createDatasetMetadata", params=params, data=payload)

    @check_capability_availability
    def get_dataset(
        self,
        collection_name: ObjectStorageModel.CollectionName,
        dataset_name: ObjectStorageModel.DatasetName,
    ):
        params = {"collection_name": collection_name, "dataset_name": dataset_name}
        return self._client.get("getDataset", params=params).json()

    # TODO: check implementation
    def create_or_replace_dataset(
        self,
        request: Request,
        file: UploadFile,
        collection_name: ObjectStorageModel.CollectionName,
        dataset_name: ObjectStorageModel.DatasetName = None,
    ) -> ObjectStorageModel.DatasetCreateResponse:
        params = {"collection_name": collection_name}
        if dataset_name:
            params.update({"dataset_name": dataset_name})
        return ObjectStorageModel.DatasetCreateResponse(
            **self._client.put(
                "createOrReplaceDataset",
                params=params,
                headers=request.headers,
                data=file.file,
            )
        )

    # TODO: check implementation
    @check_capability_availability
    def create_or_replace_dataset_metadata(
        self,
        collection_name: ObjectStorageModel.CollectionName,
        dataset_name: ObjectStorageModel.DatasetName,
        payload=None,
    ):
        params = {"collection_name": collection_name, "dataset_name": dataset_name}
        return self._client.post(
            "createOrReplaceDatasetMetadata", params=params, data=payload
        )

    @check_capability_availability
    def delete_dataset(
        self,
        collection_name: ObjectStorageModel.CollectionName,
        dataset_name: ObjectStorageModel.DatasetName,
    ):
        params = {"collection_name": collection_name, "dataset_name": dataset_name}
        return self._client.delete("deleteDataset", params=params).json()

    # TODO: check implementation
    @check_capability_availability
    def get_dataset_metadata(
        self,
        collection_name: ObjectStorageModel.CollectionName,
        dataset_name: ObjectStorageModel.DatasetName,
    ):
        params = {"collection_name": collection_name, "dataset_name": dataset_name}
        response_headers: dict = self._client.get(
            "getDatasetMetadata", params=params
        ).headers
        return json.dumps(
            dict(
                filter(
                    lambda val: str(val[0]).startswith("X-Object-Meta"),
                    response_headers.items(),
                )
            )
        )

    @check_capability_availability
    def list_semantic_mappings(
        self, limit: int = 100, offset: int = 0
    ) -> ObjectStorageModel.SemanticMappingListResponse:
        params = {"limit": limit, "offset": offset}
        return ObjectStorageModel.SemanticMappingListResponse(
            **self._client.get("/listSemanticMappings", params=params).json()
        )

    @check_capability_availability
    def get_semantic_mapping(
        self, semantic_mapping_id: str
    ) -> ObjectStorageModel.SemanticMappingModel:
        params = {"semantic_mapping_id": semantic_mapping_id}
        return ObjectStorageModel.SemanticMappingModel.parse_obj(
            json.loads(self._client.get("getSemanticMapping", params=params))
        )
