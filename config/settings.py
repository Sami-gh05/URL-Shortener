"""Settings loader for the url-shortener application.

Uses python-dotenv to load environment variables. Provides defaults and
validates core numeric limits used by repositories and services.
"""
from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    """Immutable settings loaded from environment.

    Attributes:
        MAX_PROJECTS: upper bound for allowed projects in memory
        MAX_TASKS: upper bound for allowed tasks per project in memory
        
        MAX_NAME_LEN: upper bound for length of name of each task or project
        MAX_DESCRIPTION_LEN: upper bound for length of description of each task or project
    """

    DATABASE_URL: Optional[str] = None
    DB_USER: Optional[str] = None
    DB_PASS: Optional[str] = None
    DB_HOST: Optional[str] = None
    DB_PORT: Optional[int] = 5555
    DB_NAME: Optional[str] = None
    

    @staticmethod
    def _parse_int(value: Optional[str], fallback: int) -> int:
        try:
            return int(value) if value is not None else fallback
        except (TypeError, ValueError):
            return fallback

    @classmethod
    def load(cls) -> "Settings":
        """Load settings from environment and .env file.

        Precedence: .env -> OS environment -> dataclass defaults.
        """
        load_dotenv()
        DB_USER = os.getenv("DB_USER")
        DB_PASS = os.getenv("DB_PASS")
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = cls._parse_int(os.getenv("DB_PORT"), fallback=cls.DB_PORT)
        DB_NAME = os.getenv("DB_NAME")
        
        DATABASE_URL = f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

        return cls(DATABASE_URL=DATABASE_URL, DB_USER=DB_USER, DB_PASS=DB_PASS, DB_HOST=DB_HOST, DB_PORT=DB_PORT, DB_NAME=DB_NAME)

