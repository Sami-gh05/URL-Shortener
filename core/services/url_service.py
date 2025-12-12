"""URL service with business logic."""
from __future__ import annotations

from typing import Optional

from core.models.url_model import UrlModel
from core.repositories.url_repository import UrlRepository

class UrlService:
    """Service for URL  shortening operations."""

    #dependency injection
    def __init__(self, repository: UrlRepository):
        """Initialize the URL service with a repository."""
        self.repository = repository

    def get_url_model(self, short_code: str) -> Optional[UrlModel]:
        """Get a URL object by its short code."""
        return self.repository.get_url_model(short_code)

    def get_Original_url(self, short_code: str) -> Optional[str]:
        """Get Original URL by its short code"""
        url_model = self.get_url_model(short_code)
        if url_model is None:
            return None
        return url_model.original_url

    def delete_url(self, short_code: str) -> bool:
        """Delete a URL by its short code."""
        return self.repository.delete_url(short_code)