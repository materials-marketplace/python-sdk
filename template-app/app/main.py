from typing import Any, Callable

import requests
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, Response

from marketplace.models import (
    DatasetCreateResponse,
    DatasetId,
    DatasetModel,
    NewTransformationModel,
    TransformationCreateResponse,
    TransformationId,
    TransformationModel,
    TransformationStatusResponse,
    TransformationUpdateModel,
    TransformationUpdateResponse,
)
from marketplace.security import AuthTokenBearer


async def catch_authentication_request_errors_middleware(
    request: Request, call_next: Callable
):
    "Catch authentication requests errors to the semantic service and respond with 401."
    try:
        return await call_next(request)
    except requests.exceptions.HTTPError as error:
        if error.response.status_code == 401:
            return Response("Not authenticated.", status_code=401)
        raise


class MarketPlaceAPI(FastAPI):
    def openapi(self) -> dict[str, Any]:
        openapi_schema = super().openapi()
        openapi_schema["info"]["x-application-name"] = "MarketPlace Template App"
        return openapi_schema


app = MarketPlaceAPI(
    title="Marketplace Template App",
    description="This is a template app for the Materials Marketplace.",
    version="0.1.0",
    contact={
        "name": "My organization",
        "url": "https://www.example.com/contact",
        "email": "mail@example.com",
    },
    dependencies=[Depends(AuthTokenBearer())],
    servers=[{"url": "https://marketplace.example.com"}],
)
app.middleware("http")(catch_authentication_request_errors_middleware)


@app.get(
    "/",
    operation_id="frontend",
    tags=["FrontPage"],
    responses={
        404: {"description": "Not found."},
        401: {"description": "Not authenticated."},
        500: {"description": "Internal server error."},
        503: {"description": "Service unavailable."},
    },
    response_class=HTMLResponse(),
)
async def frontpage() -> HTMLResponse:
    """Open the frontpage of the app."""
    raise HTTPException(status_code=404, detail="Not found.")


@app.get(
    "/health",
    operation_id="heartbeat",
    tags=["System"],
    response_class=HTMLResponse,
    responses={
        401: {"description": "Not authenticated."},
        500: {"description": "Internal server error."},
        503: {"description": "Service unavailable."},
    },
)
async def heartbeat() -> HTMLResponse:
    """Check whether the application is running and available."""
    return HTMLResponse(content="<html><body>OK</body></html>", status_code=200)


@app.post(
    "/dataset",
    operation_id="createDataset",
    tags=["DataSink"],
    response_model=DatasetCreateResponse,
    responses={
        401: {"description": "Not authenticated."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def create_dataset(dataset: DatasetModel) -> DatasetCreateResponse:
    """Create a new dataset."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@app.get(
    "/dataset/{dataset_id}",
    operation_id="getDataset",
    tags=["DataSource"],
    response_class=JSONResponse,
    response_model=DatasetModel,
    responses={
        401: {"description": "Not authenticated."},
        404: {"description": "Not found."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def get_dataset(dataset_id: DatasetId) -> DatasetModel:
    """Retrieve an existing data set."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@app.post(
    "/transformation",
    operation_id="newTransformation",
    tags=["Transformation"],
    response_model=TransformationCreateResponse,
    responses={
        401: {"description": "Not authenticated."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def create_transformation(
    transformation: NewTransformationModel,
) -> TransformationCreateResponse:
    """Create a new transformation."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@app.get(
    "/transformation/{transformation_id}",
    operation_id="getTransformation",
    tags=["Transformation"],
    response_model=TransformationModel,
    responses={
        401: {"description": "Not authenticated."},
        404: {"description": "Not found."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def get_transformation(
    transformation_id: TransformationId,
) -> TransformationModel:
    """Retrieve an existing transformation."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@app.delete(
    "/transformation/{transformation_id}",
    operation_id="deleteTransformation",
    tags=["Transformation"],
    status_code=204,
    responses={
        401: {"description": "Not authenticated."},
        404: {"description": "Not found."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def delete_transformation(
    transformation_id: TransformationId,
) -> HTTPException | None:
    """Delete an existing transformation."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@app.patch(
    "/transformation/{transformation_id}",
    operation_id="updateTransformation",
    tags=["Transformation"],
    response_model=TransformationUpdateResponse,
    responses={
        401: {"description": "Not authenticated."},
        404: {"description": "Not found."},
        409: {
            "description": "The requested state is unavailable (example: trying to stop an already completed transformation)."
        },
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def update_transformation(
    id: TransformationId, update: TransformationUpdateModel
) -> TransformationUpdateResponse:
    """Update an existing transformation."""
    raise HTTPException(status_code=501, detail="Not implemented.")


# @app.post(
#     "/transformation/{transformation_id}/run",
#     operation_id="startTransformation",
#     tags=["Transformation"],
#     response_model=TransformationUpdateResponse,
#     responses={
#         401: {"description": "Not authenticated."},
#         500: {"description": "Internal server error."},
#         501: {"description": "Not implemented."},
#         503: {"description": "Service unavailable."},
#     },
# )
# def start_transformation(
#     transformation_id: TransformationId,
# ) -> TransformationStatusResponse:
#     """Start a transformation."""
#     raise HTTPException(status_code=501, detail="Not implemented.")


# @app.post(
#     "/transformation/{transformation_id}/stop",
#     operation_id="stopTransformation",
#     tags=["Transformation"],
#     status_code=204,
#     responses={
#         401: {"description": "Not authenticated."},
#         500: {"description": "Internal server error."},
#         501: {"description": "Not implemented."},
#         503: {"description": "Service unavailable."},
#     },
# )
# def stop_transformation(transformation_id: TransformationId) -> None:
#     """Stop a transformation."""
#     raise HTTPException(status_code=501, detail="Not implemented.")


@app.get(
    "/transformation/{transformation_id}/status",
    operation_id="getTransformationStatus",
    tags=["Transformation"],
    response_model=TransformationStatusResponse,
    responses={
        401: {"description": "Not authenticated."},
        404: {"description": "Not found."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def get_transformation_status(
    transformation_id: TransformationId,
) -> TransformationStatusResponse:
    """Retrieve the status of a transformation."""
    raise HTTPException(status_code=501, detail="Not implemented.")


@app.get(
    "/transformation",
    operation_id="getTransformationList",
    tags=["Transformation"],
    response_model=list[TransformationModel],
    responses={
        401: {"description": "Not authenticated."},
        500: {"description": "Internal server error."},
        501: {"description": "Not implemented."},
        503: {"description": "Service unavailable."},
    },
)
async def list_transformation() -> list[TransformationModel]:
    """Retrieve a list of transformations."""
    raise HTTPException(status_code=501, detail="Not implemented.")
