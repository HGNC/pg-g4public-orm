"""Sphinx configuration for pg-g4public-orm.

This config powers the docs build invoked by ``docs.yml``/``pages.yml``::

    cd docs && python -m sphinx -W -b html . _build/html
"""

from __future__ import annotations

import os
import sys
from datetime import datetime

# ---------------------------------------------------------------------------
# Path setup
#
# Make the in-tree package importable for ``sphinx.ext.autodoc`` regardless of
# the current working directory (paths resolved relative to this file so the
# build is identical whether invoked from ``docs/`` or the repo root).
# ---------------------------------------------------------------------------
_conf_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(_conf_dir, "..")))
sys.path.insert(0, os.path.abspath(os.path.join(_conf_dir, "..", "src")))

project = "pg-g4public-orm"
author = "HGNC Development Team"
year = datetime.now().year
copyright = f"{year}, {author}"

# The release/short version rendered in the docs header; kept in sync with the
# package version in pyproject.toml. The autodoc'd modules carry full detail.
version = "0.1"
release = "0.1.0"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
]

# MyST (Markdown) extensions — ``colon_fence`` enables ::: admonitions.
myst_enable_extensions = [
    "colon_fence",
]

# No custom templates; alabaster ships its own.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "alabaster"
html_static_path = ["_static"]

# ---------------------------------------------------------------------------
# Autodoc defaults
# ---------------------------------------------------------------------------
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "show-inheritance": True,
}
autodoc_member_order = "bysource"

# Napoleon renders Google/NumPy-style docstrings (used by the Repository).
napoleon_google_docstring = True
napoleon_numpy_docstring = False

# ---------------------------------------------------------------------------
# Intersphinx — cross-link to the canonical upstream references.
# ---------------------------------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "sqlalchemy": ("https://docs.sqlalchemy.org/en/20", None),
}
