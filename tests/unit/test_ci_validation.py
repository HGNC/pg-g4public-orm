"""Validation tests for CI workflows and release scripts.

Task T17 verifies that the GitHub Actions workflows are actionlint-clean and
that release helper scripts execute over real repository history.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPECTED_BUMPS = {"major", "minor", "patch", "none"}


def _run_command(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
        timeout=120,
    )


def _assert_command_success(
    result: subprocess.CompletedProcess[str], command_name: str
) -> None:
    assert result.returncode == 0, (
        f"{command_name} failed:\n"
        f"--- stdout ---\n{result.stdout}\n"
        f"--- stderr ---\n{result.stderr}"
    )


def test_actionlint_passes_for_all_workflows() -> None:
    """Workflows must pass static validation before pushing to main."""
    actionlint = shutil.which("actionlint")
    assert actionlint is not None, (
        "actionlint binary not found; install test dependencies first "
        "(e.g. `uv sync --extra test`)."
    )

    actionlint_result = _run_command([actionlint])
    _assert_command_success(actionlint_result, "actionlint")


def test_release_scripts_run_on_real_history(tmp_path: Path) -> None:
    """Release analysis scripts should run end-to-end over HEAD history."""
    analysis_path = tmp_path / "analysis.json"

    analyze_result = _run_command(
        [
            sys.executable,
            ".github/scripts/analyze_commits.py",
            "--range",
            "HEAD",
            "--output",
            str(analysis_path),
        ]
    )
    _assert_command_success(analyze_result, "analyze_commits.py")
    assert analysis_path.exists(), "analyze_commits.py did not create analysis output"

    analysis_payload = json.loads(analysis_path.read_text(encoding="utf-8"))
    assert "stats" in analysis_payload
    assert "summary" in analysis_payload

    bump_result = _run_command(
        [
            sys.executable,
            ".github/scripts/determine_version_bump.py",
            str(analysis_path),
        ]
    )
    _assert_command_success(bump_result, "determine_version_bump.py")

    bump = bump_result.stdout.strip()
    assert bump in EXPECTED_BUMPS
