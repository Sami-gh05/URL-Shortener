"""URL repository interface for SQLAlchemy."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from core.models.url_model import UrlModel

class UrlRepository(ABC):
    """Abstract interface for URL repository operations.

    This interface defines the contract that all URL repository implementations
    must follow, following the Dependency Inversion Principle.
    """

    @abstractmethod
    def get_url_model(self, short_code: str) -> Optional[UrlModel]:
        """Get a URL object by its short code.

        returns None if the URL is not found."""

        pass


    @abstractmethod
    def delete_url(self, short_code: str) -> bool:
        """Delete a URL by its short code.

        returns false if the URL is not found."""

        pass
