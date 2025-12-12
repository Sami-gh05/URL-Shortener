"""SQL implementation of URL repository for database operations."""
from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from core.models.url_model import UrlModel
from core.repositories.url_repository import IUrlRepository


class SqlUrlRepository(IUrlRepository):
    """Repository for URL database operations."""

    def __init__(self, session: Session):
        """Initialize repository with database session."""
        self.session = session

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
        url = UrlModel(original_url=original_url, short_code=short_code)
        self.session.add(url)
        self.session.flush()
        self.session.refresh(url)
        return url

    def get_all(self) -> list[UrlModel]:
        """Get all URL records.

        Returns:
            List of all UrlModel instances, ordered by created_at descending
        """
        return self.session.query(UrlModel).order_by(UrlModel.created_at.desc()).all()

    def find_by_short_code(self, short_code: str) -> Optional[UrlModel]:
        """Find a URL by its short code.

        Args:
            short_code: The short code to search for

        Returns:
            UrlModel if found, None otherwise
        """
        return self.session.query(UrlModel).filter(UrlModel.short_code == short_code).first()
