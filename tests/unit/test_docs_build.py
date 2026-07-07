"""Tests that the Sphinx documentation site builds cleanly.

These mirror the exact invocation used by the ``docs.yml``/``pages.yml``
workflows: ``python -m sphinx -W -b html . _build/html`` run from ``docs/``.
Warnings-as-errors (``-W``) means the build fails on any autodoc/conf warning,
so this guards the API reference against drift (missing modules, bad autodoc
targets, broken reStructuredText/Markdown) as well as malformed config.
"""

from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
DOCS_DIR = ROOT / "docs"
BUILD_DIR = DOCS_DIR / "_build"
HTML_DIR = BUILD_DIR / "html"


def _run_sphinx() -> subprocess.CompletedProcess[str]:
    """Invoke sphinx exactly as docs.yml/pages.yml do (warnings-as-errors)."""
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "sphinx",
            "-W",
            "-b",
            "html",
            ".",
            "_build/html",
        ],
        cwd=str(DOCS_DIR),
        capture_output=True,
        text=True,
        timeout=300,
    )


@pytest.fixture(scope="module")
def sphinx_build():
    """Build the docs once for the module; clean before and after."""
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    result = _run_sphinx()
    yield result
    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)


def test_docs_tree_exists():
    """The Sphinx config and content required by T14 must exist (RED guard)."""
    assert (DOCS_DIR / "conf.py").is_file(), "docs/conf.py is missing"
    assert (DOCS_DIR / "index.md").is_file(), "docs/index.md is missing"
    assert (DOCS_DIR / "installation.md").is_file(), "docs/installation.md is missing"
    assert (DOCS_DIR / "quick-start.md").is_file(), "docs/quick-start.md is missing"
    assert (DOCS_DIR / "Makefile").is_file(), "docs/Makefile is missing"
    assert (
        DOCS_DIR / "_static" / ".gitkeep"
    ).is_file(), "docs/_static/.gitkeep is missing"
    assert (DOCS_DIR / "api" / "index.rst").is_file(), "docs/api/index.rst is missing"
    assert (DOCS_DIR / "api" / "models.rst").is_file(), "docs/api/models.rst is missing"


def test_docs_build_with_warnings_as_errors(sphinx_build):
    """The exact docs.yml/pages.yml invocation must exit 0."""
    assert sphinx_build.returncode == 0, (
        f"Sphinx build failed (rc={sphinx_build.returncode}):\n"
        f"--- stdout ---\n{sphinx_build.stdout}\n"
        f"--- stderr ---\n{sphinx_build.stderr}"
    )
    assert (HTML_DIR / "index.html").is_file(), "index.html was not generated"


def test_docs_autodoc_pg_g4public_orm(sphinx_build):
    """The built API reference must autodoc the pg_g4public_orm package."""
    assert sphinx_build.returncode == 0
    models_html = (HTML_DIR / "api" / "models.html").read_text(encoding="utf-8")
    assert (
        "PubHgnc" in models_html
    ), "pg_g4public_orm models are not autodoc'd in api/models.html"
    # The project name from conf.py is rendered into the landing page header.
    index_html = (HTML_DIR / "index.html").read_text(encoding="utf-8")
    assert "pg-g4public-orm" in index_html
