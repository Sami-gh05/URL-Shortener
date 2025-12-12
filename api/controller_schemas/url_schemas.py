"""Pydantic schemas for URL endpoints."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, model_validator

class UrlResponse(BaseModel):
    """Response schema for URL endpoints."""

    id: int
    original_url: str
    short_code: str
    created_at: datetime

    class Config:
        """pydantic config."""
        from_attributes = True


class RedirectResponse(BaseModel):
    """Redirect response schema."""
    status: str = Field(default="success")
    url: str


class SuccessGetResponse(BaseModel):
    """Success response schema."""

    status: str = Field(default="success")
    data: UrlResponse

class SuccessDeleteResponse(BaseModel):
    """Success response schema."""

    status: str = Field(default="success")
    url: str
    message: str = Field(default="")

    @model_validator(mode='after')
    def set_message(self):
        """Set the message based on the url field."""
        if not self.message:
            self.message = f"{self.url} deleted successfully"
        return self


class FailureResponse(BaseModel):
    """Failure response schema."""

    status: str = Field(default="failure")
    message: str