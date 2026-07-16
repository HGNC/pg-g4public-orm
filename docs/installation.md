# Installation

`pg-g4public-orm` requires Python ≥ 3.13 and a PostgreSQL database with the
`g4public` schema already loaded.

## From source (development)

The project uses [`uv`](https://docs.astral.sh/uv/) for environment management.

```bash
git clone https://github.com/HGNC/pg-g4public-orm.git
cd pg-g4public-orm
uv sync --group dev --extra dev
```

This installs two complementary sets of dev tooling:

- the **`dev` extra** (declared in `[project.optional-dependencies]`) — the
  quality toolchain (`mypy`, `ruff`, `black`, `isort`, `bandit`), plus the
  `test` and `postgres` extras transitively;
- the **`dev` dependency-group** (declared in `[dependency-groups]`) — the docs
  build toolchain (`sphinx`, `myst-parser`) and `anybadge`/`testcontainers`.

`uv sync` includes the default `dev` group automatically, so `uv sync --extra dev`
also works; the explicit `--group dev --extra dev` form (used by the CI docs
workflow) documents the intent and guarantees the docs build is available.

## Runtime dependencies

- [SQLAlchemy](https://www.sqlalchemy.org/) ≥ 2.0 — declarative ORM core.
- [psycopg](https://www.psycopg.org/psycopg3/) ≥ 3.1 (`psycopg[binary]`) — the
  `postgresql+psycopg` driver (db-common-canonical; psycopg3, not psycopg2).
- [pydantic](https://docs.pydantic.dev/) ≥ 2.0 and
  [pydantic-settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/) ≥ 2.0
  — typed settings.
- [db-common](https://github.com/HGNC/db-common) ≥ 0.2.0 — shared engine /
  session factory and declarative base.

## Configuration

Settings are read from `DB_`-prefixed environment variables (or a `.env`
file). PostgreSQL defaults: `driver=postgresql+psycopg`, `port=5432`,
`database=g4public` (PostgreSQL ignores `charset`, so it is not used). See
[`.env.example`](https://github.com/HGNC/pg-g4public-orm/blob/main/.env.example)
for the full list.

## Running the test suite

```bash
uv run pytest                         # unit tests only (mocked sessions)
uv run pytest -m integration          # + ephemeral PostgreSQL container
```

Integration tests require Docker (they spin up a `postgres:16` testcontainer)
and are skipped automatically when Docker / Postgres is unavailable.

## Building the docs

```bash
cd docs && uv run python -m sphinx -W -b html . _build/html
```

This is the exact invocation used by the `docs.yml` / `pages.yml` workflows
(warnings-as-errors via `-W`); it requires the docs toolchain, so run it after
`uv sync --group dev --extra dev`.
