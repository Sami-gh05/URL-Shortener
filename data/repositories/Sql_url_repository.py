"""SQLAlchemy implementation of the URL repository interface."""

from __future__ import annotations

from typing import Optional

from sqlalchemy.orm import Session

from core.models.url_model import UrlModel
from core.repositories.url_repository import UrlRepository


class SqlUrlRepository(UrlRepository):
    """SQLAlchemy implementation of the URL repository interface."""
    
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
      
      

    def get_url_model(self, short_code: str) -> Optional[UrlModel]:
        """Get a URL by its short code."""
        return self.session.query(UrlModel).filter(UrlModel.short_code == short_code).first()

    def delete_url(self, short_code: str) -> bool:
        """Delete a URL by its short code.
        
        Note: Does not commit the transaction. The session dependency
        will handle commit/rollback automatically.
        """
        url = self.get_url_model(short_code)
        if url is None:
            return False
        self.session.delete(url)
        # Don't commit here - let the session dependency handle it
        # This ensures proper transaction management and rollback on errors
        return True
        
