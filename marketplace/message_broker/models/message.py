from typing import Any, Dict, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    endpoint: str = Field(None, description="API endpoint of the application")
    body_base64: str = Field(None, description="A base64-encrypted body")
    body: Optional[Any] = Field(None, description="The message payload")
    query_params: Optional[Dict[str, str]] = Field(None, description="Query parameters")