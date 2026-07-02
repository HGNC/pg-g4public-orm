# pg-g4public-orm

SQLAlchemy 2.0 ORM for the PostgreSQL `g4public` database (HGNC public
gene/family data). Synchronous only, built on the shared
[`db-common`](https://github.com/HGNC/db-common) library using the
`postgresql+psycopg` (psycopg3) driver.

> The ORM reads and writes **data only** — it never creates, alters, or drops
> schema objects.

## Status

Scaffold (Task T1): `core` package (`DatabaseSettings`, session module-function
surface, `DeclarativeBase`) on `db-common`. Models, repositories, integration
harness, CI/CD, and docs land in subsequent tasks.

## Quick start

```python
from pg_g4public_orm import DatabaseSettings, initialize_engine, get_readwrite_session

initialize_engine(DatabaseSettings())  # reads DB_* env vars

with get_readwrite_session() as session:
    ...
```

## Configuration

Settings are read from `DB_`-prefixed environment variables (or a `.env` file).
PostgreSQL defaults: `driver=postgresql+psycopg`, `port=5432`,
`database=g4public`. See [`.env.example`](.env.example).
