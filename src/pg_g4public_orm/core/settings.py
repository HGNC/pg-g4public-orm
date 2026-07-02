"""PostgreSQL database configuration settings (db-common subclass).

This mirrors ``vgnc_orm/core/settings.py`` but carries **PostgreSQL** defaults
(``postgresql+psycopg`` / port ``5432`` / database ``g4public``). The
``charset``/``collation`` fields are inherited from db-common but are inert for
PostgreSQL (db-common's ``EngineFactory`` only applies them to MySQL drivers),
so they are neither declared nor used here.
"""

from typing import Any

import db_common
from pydantic import AliasChoices, Field, model_validator
from pydantic_settings import SettingsConfigDict


class DatabaseSettings(db_common.DatabaseSettings):
    """Database connection settings for the PostgreSQL ``g4public`` database.

    Loads from ``DB_``-prefixed environment variables (or a ``.env`` file) and
    delegates URL construction and shared pool settings to db-common.

    The ``DB_NAME`` / ``DB_DATABASE`` and ``DB_USER`` / ``DB_USERNAME`` aliases
    are accepted for parity with the sibling ORMs.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix="DB_",
        env_nested_max_split=1,
        extra="ignore",
        populate_by_name=True,
    )

    driver: str = Field(
        default="postgresql+psycopg",
        description="SQLAlchemy driver string (psycopg3)",
    )
    host: str = Field(default="localhost", description="Database host")
    port: int = Field(default=5432, description="Database port (PostgreSQL default)")
    database: str = Field(
        default="g4public",
        validation_alias=AliasChoices("DB_NAME", "DB_DATABASE"),
        description="Database name",
    )
    username: str = Field(
        default="",
        validation_alias=AliasChoices("DB_USER", "DB_USERNAME"),
        description="Database user",
    )
    password: str = Field(default="", description="Database password")
    pool_size: int = Field(default=5, description="Connection pool size")
    max_overflow: int = Field(default=10, description="Max overflow for pool")

    # -- Legacy aliases (parity with the sibling ORMs) -----------------------
    @property
    def name(self) -> str:
        """Legacy alias for :attr:`database`."""
        return self.database

    @name.setter
    def name(self, value: str) -> None:
        self.database = value

    @property
    def user(self) -> str:
        """Legacy alias for :attr:`username`."""
        return self.username

    @user.setter
    def user(self, value: str) -> None:
        self.username = value

    @model_validator(mode="before")
    @classmethod
    def _map_legacy_constructor_kwargs(cls, data: Any) -> Any:
        """Map legacy constructor kwargs (name, user) to canonical fields.

        Legacy keys are only remapped when actually present, so absent keys
        never inject ``None`` and clobber the field defaults.
        """
        if isinstance(data, dict):
            if "name" in data:
                data.setdefault("database", data.pop("name"))
            if "user" in data:
                data.setdefault("username", data.pop("user"))
        return data

    @property
    def url(self) -> str:
        """Build the PostgreSQL connection URL as a legacy string."""
        return self.get_url().render_as_string(hide_password=False)
