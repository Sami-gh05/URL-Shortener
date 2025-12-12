"""Pydantic schemas for URL endpoints."""
from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class CreateUrlRequest(BaseModel):
    """Request schema for creating a short URL."""

    original_url: str = Field(..., description="The original URL to shorten", min_length=1)

    class Config:
        """Pydantic config."""

        json_schema_extra = {
            "example": {
                "original_url": "https://example.com",
            }
        }


class UrlResponse(BaseModel):
    """Response schema for a single URL."""

    id: int
    original_url: str
    short_code: str
    created_at: datetime

    class Config:
        """Pydantic config."""

        from_attributes = True


class SuccessResponse(BaseModel):
    """Success response wrapper."""

    status: str = "success"
    data: UrlResponse


class SuccessListResponse(BaseModel):
    """Success response wrapper for lists."""

    status: str = "success"
    data: list[UrlResponse]


class FailureResponse(BaseModel):
    """Failure response wrapper."""

    status: str = "failure"
    message: str

