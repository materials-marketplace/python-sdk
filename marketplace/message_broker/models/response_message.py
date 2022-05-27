from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class ResponseMessage(BaseModel):
    response_code: int = Field(200, description="The HTTP response code")
    body_base64: str = Field(None, description="A base64-encrypted body")
    body: Optional[Any] = Field(None, description="The response message payload")
    headers: Optional[Dict[str, str]] = Field(None, description="Response headers")
