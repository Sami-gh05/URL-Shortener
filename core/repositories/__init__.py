"""Core repository interfaces package.

This package contains repository interface definitions that define the contract
for data access operations, following the Repository pattern.
"""
from core.repositories.url_repository import IUrlRepository

__all__ = ["IUrlRepository"]
