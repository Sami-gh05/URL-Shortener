"""URL model for SQLAlchemy."""
from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import Column, Integer, String, DateTime

from data.db.sql_db_base import Base


class UrlModel(Base):
    """URL model representing shortened URLs in the database."""

    __tablename__ = "urls"

    id = Column(Integer, primary_key=True, autoincrement=True)
    original_url = Column(String, nullable=False)
    short_code = Column(String(10), unique=True, nullable=False, index=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self) -> str:
        """String representation of the model."""
        return f"<UrlModel(id={self.id}, short_code='{self.short_code}', original_url='{self.original_url}')>"
