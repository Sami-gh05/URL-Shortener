"""URL controller for FastAPI endpoints (fixed routes)."""
from __future__ import annotations

from typing import Annotated

from starlette.responses import RedirectResponse, JSONResponse
from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.responses import RedirectResponse as HTTPRedirectResponse, Response
from api.controller_schemas.url_schemas import UrlResponse, SuccessGetResponse, SuccessDeleteResponse, FailureResponse

from core.services.url_service import UrlService

from sqlalchemy.orm import Session
from data.db.session import get_db_session
from data.repositories.Sql_url_repository import SqlUrlRepository

router = APIRouter()

def get_url_service(
    session: Annotated[Session, Depends(get_db_session)],
) -> UrlService:
    repository = SqlUrlRepository(session)
    return UrlService(repository)


@router.get(
    "/urls/{short_code}",
    response_model=SuccessGetResponse,
    status_code=status.HTTP_200_OK,
    responses={
        404: {"model": FailureResponse, "description": "URL not found"},
        500: {"model": FailureResponse, "description": "Internal server error"},
    },
)
def get_url_by_short_code(
    short_code: str,
    service: Annotated[UrlService, Depends(get_url_service)]
) -> SuccessGetResponse:
    """Get the original url by short code (metadata endpoint)."""
    url_model = service.get_url_model(short_code)
    if url_model is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"status": "failure", "message": "URL not found"},
        )
    url_response = UrlResponse.model_validate(url_model)
    return SuccessGetResponse(data=url_response)


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
    url_model = service.get_url_model(short_code)
    if url_model is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"status": "failure", "message": "URL not found"},
        )

    original = url_model.original_url
    return RedirectResponse(url=original, status_code=302)


@router.delete(
    "/urls/{short_code}",
    responses={
        204: {"description": "URL deleted successfully"},
        404: {"model": FailureResponse, "description": "URL not found"},
        500: {"model": FailureResponse, "description": "Internal server error"},
    },
    status_code=status.HTTP_204_NO_CONTENT,  # declares default success code
)
def delete_by_short_code(
    short_code: str,
    service: Annotated[UrlService, Depends(get_url_service)],
):
    """Delete a shortened URL by its short code."""
    # Check existence first (so we can return 404 if missing)
    url_model = service.get_url_model(short_code)
    if url_model is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"status": "failure", "message": "URL not found"},
        )

    delete_status: bool = service.delete_url(short_code)
    if delete_status:
        # 204 No Content must have an empty body
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    # If deletion failed for internal reasons
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"status": "failure", "message": "Failed to delete URL"},
    )
