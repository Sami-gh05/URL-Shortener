"""Abstract repository interface for URL operations."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from core.models.url_model import UrlModel

class IUrlRepository(ABC):
    """Abstract interface for URL repository operations.

    This interface defines the contract that all URL repository implementations
    must follow, following the Dependency Inversion Principle.
    """

    @abstractmethod
    def create(self, original_url: str, short_code: str) -> UrlModel:
        """Create a new URL record.

        Args:
            original_url: The original URL to shorten
            short_code: The generated short code

        Returns:
            The created UrlModel instance

        Raises:
            IntegrityError: If short_code already exists
        """
        pass

    @abstractmethod
    def get_all(self) -> list[UrlModel]:
        """Get all URL records.

        Returns:
            List of all UrlModel instances, ordered by created_at descending
        """
        pass

    @abstractmethod
    def find_by_short_code(self, short_code: str) -> Optional[UrlModel]:
        """Find a URL by its short code.

        Args:
            short_code: The short code to search for

        Returns:
            UrlModel if found, None otherwise
        """
        pass

    @abstractmethod
    def get_url_model(self, short_code: str) -> Optional[UrlModel]:
        """Get a URL object by its short code.

        Args:
            short_code: The short code to search for

        Returns:
            UrlModel if found, None otherwise
        """
        pass


    @abstractmethod
    def delete_url(self, short_code: str) -> bool:
        """Delete a URL by its short code.

        returns false if the URL is not found."""

        pass
