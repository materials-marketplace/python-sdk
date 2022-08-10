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
        return ObjectStorageModel.CollectionListResponse(
            **self._client.get("/data").json()
        )

    @check_capability_availability
    def list_datasets(
        self, collection_name: ObjectStorageModel.CollectionName
    ) -> ObjectStorageModel.DatasetListResponse:
        return ObjectStorageModel.DatasetListResponse(
            **self._client.get(f"/{collection_name}").json()
        )

    # TODO: use request and header
    @check_capability_availability
    def create_collections(
        self,
        request: Request,
        collection_name: ObjectStorageModel.CollectionName = None,
    ):
        url = f"/{collection_name}" if collection_name else "/"
        return self._client.put(url, json=request).json()

    # TODO: return response header X-Object-Meta-name
    @check_capability_availability
    def get_collection_metadata(
        self, collection_name: ObjectStorageModel.CollectionName
    ):
        pass

    @check_capability_availability
    def delete_collection(self, collection_name: ObjectStorageModel.CollectionName):
        return self._client.delete(f"/{collection_name}").json()

    # TODO: use request and UploadFile
    # Content-type and other header parameters?
    @check_capability_availability
    def create_dataset(
        self,
        request: Request,
        file: UploadFile,
        collection_name: ObjectStorageModel.CollectionName,
        dataset_name: ObjectStorageModel.DatasetName = None,
    ) -> ObjectStorageModel.DatasetCreateResponse:
        base_url = f"/{collection_name}/"
        url = f"{base_url}{dataset_name}" if dataset_name else base_url
        return ObjectStorageModel.DatasetCreateResponse(
            **self._client.put(url, file.file)
        )

    # TODO: add to header
    @check_capability_availability
    def create_or_replace_dataset_metadata(
        self,
        collection_name: ObjectStorageModel.CollectionName,
        dataset_name: ObjectStorageModel.DatasetName = None,
    ):
        pass

    # TODO: add to header
    @check_capability_availability
    def get_dataset_metadata(
        self,
        collection_name: ObjectStorageModel.CollectionName,
        dataset_name: ObjectStorageModel.DatasetName,
    ):
        pass

    @check_capability_availability
    def get_dataset(
        self,
        collection_name: ObjectStorageModel.CollectionName,
        dataset_name: ObjectStorageModel.DatasetName,
    ):
        return self._client.get(f"/{collection_name}/{dataset_name}").json()

    @check_capability_availability
    def delete_dataset(
        self,
        collection_name: ObjectStorageModel.CollectionName,
        dataset_name: ObjectStorageModel.DatasetName,
    ):
        return self._client.delete(f"/{collection_name}/{dataset_name}").json()

    @check_capability_availability
    def list_semantic_mappings(
        self, limit: int = 100, offset: int = 0
    ) -> ObjectStorageModel.SemanticMappingListResponse:
        return ObjectStorageModel.SemanticMappingListResponse(
            **self._client.get("/semanticMappings").json()
        )

    @check_capability_availability
    def get_semantic_mapping(
        self, semantic_mapping_id: str
    ) -> ObjectStorageModel.SemanticMappingModel:
        return ObjectStorageModel.SemanticMappingModel.parse_obj(
            json.loads(self._client.get(f"/semanticMappings/{semantic_mapping_id}"))
        )
