"""Packaging: the PEP 561 ``py.typed`` marker ships inside the built wheel.

Consumers only benefit from pg-g4public-orm's inline type annotations if the
``py.typed`` marker is actually packaged (PEP 561). A packaging test is the
only authoritative check: it builds the real wheel and inspects its namelist.
"""

import subprocess
import zipfile
from pathlib import Path

# The repo root (parent of this tests/ directory) is where ``uv build`` must
# run to find pyproject.toml.
REPO_ROOT = Path(__file__).resolve().parent.parent


def test_py_typed_in_wheel(tmp_path: Path) -> None:
    """The ``py.typed`` marker must be present in the built wheel's namelist.

    Builds the wheel into an isolated temp dir (so the working tree is never
    polluted) and asserts the marker ships under its package path.
    """
    result = subprocess.run(
        [
            "uv",
            "build",
            "--wheel",
            "--out-dir",
            str(tmp_path),
            "--no-create-gitignore",
        ],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, (
        f"`uv build` failed (rc={result.returncode}):\n"
        f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
    )

    wheels = sorted(tmp_path.glob("pg_g4public_orm-*.whl"))
    assert wheels, f"no pg_g4public_orm wheel produced in {tmp_path}"
    wheel = wheels[-1]

    with zipfile.ZipFile(wheel) as zf:
        namelist = zf.namelist()
    assert (
        "pg_g4public_orm/py.typed" in namelist
    ), f"py.typed marker missing from wheel {wheel.name}; namelist:\n{namelist}"
