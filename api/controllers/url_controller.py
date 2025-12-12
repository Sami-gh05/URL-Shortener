"""URL controller with FastAPI routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from api.controller_schemas.url_schemas import (
    CreateUrlRequest,
    SuccessResponse,
    SuccessListResponse,
    FailureResponse,
    UrlResponse,
)
from core.services.url_service import UrlService, InvalidUrlError
from data.db.session import get_db_session
from data.repositories.Sql_url_repository import SqlUrlRepository

router = APIRouter(prefix="/urls", tags=["urls"])


def get_url_service(session: Annotated[Session, Depends(get_db_session)]) -> UrlService:
    """Dependency to get URL service instance."""
    repository = SqlUrlRepository(session)
    return UrlService(repository)


@router.post(
    "",
    response_model=SuccessResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": FailureResponse, "description": "Invalid input"},
        500: {"model": FailureResponse, "description": "Internal server error"},
    },
)
def create_short_url(
    request: CreateUrlRequest,
    service: Annotated[UrlService, Depends(get_url_service)],
) -> SuccessResponse:
    """Create a shortened URL.

    Args:
        request: The request containing the original URL
        service: The URL service instance

    Returns:
        Success response with created URL data

    Raises:
        HTTPException: 400 for invalid input, 500 for server errors
    """
    try:
        url_model = service.create_short_url(request.original_url)
        url_response = UrlResponse.model_validate(url_model)
        return SuccessResponse(data=url_response)
    except InvalidUrlError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"status": "failure", "message": "Invalid URL"},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "failure", "message": f"Internal server error: {str(e)}"},
        )


@router.get(
    "",
    response_model=SuccessListResponse,
    status_code=status.HTTP_200_OK,
    responses={
        500: {"model": FailureResponse, "description": "Internal server error"},
    },
)
def get_all_urls(
    service: Annotated[UrlService, Depends(get_url_service)],
) -> SuccessListResponse:
    """Get all shortened URLs.

    Args:
        service: The URL service instance

    Returns:
        Success response with list of URLs (empty list if none exist)

    Raises:
        HTTPException: 500 for server errors
    """
    try:
        url_models = service.get_all_urls()
        url_responses = [UrlResponse.model_validate(url) for url in url_models]
        return SuccessListResponse(data=url_responses)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "failure", "message": f"Internal server error: {str(e)}"},
        )

