"""URL controller with FastAPI routes."""
from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse, Response
from starlette.responses import RedirectResponse
from sqlalchemy.orm import Session
from starlette.status import HTTP_200_OK

from api.controller_schemas import SuccessDeleteResponse
from api.controller_schemas.url_schemas import (
    CreateUrlRequest,
    SuccessGetResponse,
    SuccessListResponse,
    FailureResponse,
    UrlResponse,
)
from core.services.url_service import UrlService, InvalidUrlError
from data.db.session import get_db_session
from data.repositories.Sql_url_repository import SqlUrlRepository

router = APIRouter(prefix="/urls", tags=["urls"])

def get_url_service(
    session: Annotated[Session, Depends(get_db_session)],
) -> UrlService:
    repository = SqlUrlRepository(session)
    return UrlService(repository)


@router.post(
    "",
    response_model=SuccessGetResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": FailureResponse, "description": "Invalid input"},
        500: {"model": FailureResponse, "description": "Internal server error"},
    },
)
def create_short_url(
    request: CreateUrlRequest,
    service: Annotated[UrlService, Depends(get_url_service)],
) -> SuccessGetResponse:
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
        return SuccessGetResponse(data=url_response)
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

@router.get(
    "/{short_code}",
    response_model=SuccessGetResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": FailureResponse, "description": "URL not found"},
        500: {"model": FailureResponse, "description": "Internal server error"},
    },
)
def get_url_by_short_code(
    short_code: str,
    service: Annotated[UrlService, Depends(get_url_service)],
) -> SuccessGetResponse:
    """Get the original url by short code (metadata endpoint)."""
    try:
        url_model = service.get_url_model(short_code)
        if url_model is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"status": "failure", "message": "URL not found"},
            )
        url_response = UrlResponse.model_validate(url_model)
        return SuccessGetResponse(data=url_response)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "failure", "message": f"Internal server error: {str(e)}"},
        )


@router.get(
    "/u/{short_code}",
    responses={
        302: {"description": "Redirect to original URL"},
        404: {"model": FailureResponse, "description": "URL not found"},
        500: {"model": FailureResponse, "description": "Internal server error"},
    },
)
def redirect_to_original_url(
    short_code: str,
    service: Annotated[UrlService, Depends(get_url_service)],
):
    """Redirect to the original URL by short code (correct path: /u/{short_code})."""
    try:
        url_model = service.get_url_model(short_code)
        if url_model is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"status": "failure", "message": "URL not found"},
            )
        original = url_model.original_url
        return RedirectResponse(url=original, status_code=status.HTTP_302_FOUND)
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "failure", "message": f"Internal server error: {str(e)}"},
        )


@router.delete(
    "/{short_code}",
    responses={
        200: {"model": SuccessDeleteResponse, "description": "URL deleted successfully"},
        204: {"description": "URL deleted successfully"},
        404: {"model": FailureResponse, "description": "URL not found"},
        500: {"model": FailureResponse, "description": "Internal server error"},
    },
    status_code=status.HTTP_200_OK,
)
def delete_by_short_code(
    short_code: str,
    service: Annotated[UrlService, Depends(get_url_service)],
):
    """Delete a shortened URL by its short code."""
    try:
        # Check existence first (so we can return 404 if missing)
        url_model = service.get_url_model(short_code)
        if url_model is None:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"status": "failure", "message": "URL not found"},
            )

        original = url_model.original_url

        delete_status: bool = service.delete_url(short_code)
        if delete_status:
            # 204 No Content must have an empty body
            return SuccessDeleteResponse(url=original)

        # If deletion failed for internal reasons
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "failure", "message": "Failed to delete URL"},
        )
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"status": "failure", "message": f"Internal server error: {str(e)}"},
        )
