"""URL service with business logic."""
from __future__ import annotations

import random
import string
from typing import Optional

from sqlalchemy.exc import IntegrityError

from core.models.url_model import UrlModel
from core.repositories.url_repository import UrlRepository


class InvalidUrlError(Exception):
    """Raised when URL validation fails."""

    pass


class UrlService:
    """Service for URL shortening business logic."""

    SHORT_CODE_LENGTH = 6
    MAX_RETRIES = 10

    #dependency injection
    def __init__(self, repository: UrlRepository):
        """Initialize the URL service with a repository."""
        self.repository = repository

    def _generate_short_code(self) -> str:
        """Generate a random short code using Base62 characters.

        Returns:
            A random 6-character string
        """
        characters = string.ascii_letters + string.digits
        return "".join(random.choice(characters) for _ in range(self.SHORT_CODE_LENGTH))

    def _generate_unique_short_code(self) -> str:
        """Generate a unique short code that doesn't exist in the database.

        Returns:
            A unique short code

        Raises:
            RuntimeError: If unable to generate unique code after max retries
        """
        for _ in range(self.MAX_RETRIES):
            code = self._generate_short_code()
            if self.repository.find_by_short_code(code) is None:
                return code
        raise RuntimeError("Failed to generate unique short code after maximum retries")

    def _validate_url(self, url: str) -> None:
        """Validate that the URL is not empty and is a valid URL.

        Args:
            url: The URL to validate

        Raises:
            InvalidUrlError: If URL is invalid
        """
        if not url or not url.strip():
            raise InvalidUrlError("URL cannot be empty")

        url = url.strip()

        # Basic URL validation
        if not (url.startswith("http://") or url.startswith("https://")):
            raise InvalidUrlError("URL must start with http:// or https://")

        # Check for basic URL structure
        if "." not in url.split("://", 1)[-1]:
            raise InvalidUrlError("Invalid URL format")

    def create_short_url(self, original_url: str) -> UrlModel:
        """Create a shortened URL.

        Args:
            original_url: The original URL to shorten

        Returns:
            The created UrlModel instance

        Raises:
            InvalidUrlError: If URL is invalid
            RuntimeError: If unable to create unique short code
        """
        self._validate_url(original_url)

        short_code = self._generate_unique_short_code()

        try:
            return self.repository.create(original_url=original_url.strip(), short_code=short_code)
        except IntegrityError:
            # Retry once if there's a race condition
            short_code = self._generate_unique_short_code()
            return self.repository.create(original_url=original_url.strip(), short_code=short_code)

    def get_all_urls(self) -> list[UrlModel]:
        """Get all shortened URLs.

        Returns:
            List of all UrlModel instances
        """
        return self.repository.get_all()
      
      

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
