"""Integration fixtures for ephemeral PostgreSQL schema-loading tests."""

from collections.abc import Generator
from pathlib import Path

import psycopg
import pytest
from testcontainers.postgres import PostgresContainer


@pytest.fixture(scope="session")
def postgres_container() -> Generator[PostgresContainer]:
    """Start a postgres:16 testcontainer for integration tests."""
    with PostgresContainer("postgres:16") as container:
        yield container


@pytest.fixture(scope="session")
def schema_path() -> Path:
    """Path to the copied Navicat schema dump used by integration tests."""
    return Path(__file__).resolve().parents[2] / "schema" / "g4public.sql"


@pytest.fixture(scope="session")
def owner_stripped_schema_sql(schema_path: Path) -> str:
    """Schema SQL with all ALTER ... OWNER TO ... lines removed.

    The production dump contains ownership statements for role "genew", which
    does not exist in a clean testcontainer. We mimic:

        sed -e '/OWNER TO/d' schema/g4public.sql
    """
    original_sql = schema_path.read_text(encoding="utf-8")
    kept_lines = [line for line in original_sql.splitlines() if "OWNER TO" not in line]
    return "\n".join(kept_lines)


@pytest.fixture(scope="function")
def loaded_schema_connection(
    postgres_container: PostgresContainer,
    owner_stripped_schema_sql: str,
) -> Generator[psycopg.Connection]:
    """Open a DB connection and load the owner-stripped schema dump."""
    raw_url = postgres_container.get_connection_url()
    dsn = raw_url.replace("postgresql+psycopg2://", "postgresql://").replace(
        "postgresql+psycopg://", "postgresql://"
    )

    with psycopg.connect(dsn, autocommit=True) as conn:
        with conn.cursor() as cursor:
            cursor.execute(owner_stripped_schema_sql)
        yield conn
