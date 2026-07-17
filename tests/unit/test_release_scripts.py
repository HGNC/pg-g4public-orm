"""Tests for the release and coverage helper scripts."""

import importlib.util
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = ROOT / ".github" / "scripts"
CONFIG_PATH = ROOT / ".github" / "semantic-release-config.json"

# The 12 scripts required by the spec.
REQUIRED_SCRIPTS = [
    "analyze_commits.py",
    "determine_version_bump.py",
    "bump_version.py",
    "generate_release_notes.py",
    "update_version.py",
    "update_changelog.py",
    "update_version_references.py",
    "generate_test_summary.py",
    "generate_coverage_summary.py",
    "check_coverage_threshold.py",
    "generate_coverage_badge.py",
    "compare_coverage.py",
]


def _script_module_name(script_name: str) -> str:
    return script_name[:-3]


def _import_script_module(script_name: str):
    """Import a script module directly from .github/scripts without a package."""
    module_name = _script_module_name(script_name)
    file_path = SCRIPTS_DIR / script_name
    # Use spec_from_file_location so no __init__.py is required.
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


@pytest.mark.parametrize("script_name", REQUIRED_SCRIPTS)
def test_script_file_exists(script_name: str) -> None:
    assert (
        SCRIPTS_DIR / script_name
    ).is_file(), f"Missing script: .github/scripts/{script_name}"


def test_semantic_release_config_exists() -> None:
    assert CONFIG_PATH.is_file(), "Missing semantic-release-config.json"


@pytest.mark.parametrize("script_name", REQUIRED_SCRIPTS)
def test_script_module_imports(script_name: str) -> None:
    module = _import_script_module(script_name)
    assert module is not None


@pytest.mark.parametrize("script_name", REQUIRED_SCRIPTS)
def test_scripts_are_adapted_from_vgnc_internal_orm(script_name: str) -> None:
    """The scripts were adapted from vgnc-internal-orm and must not retain
    references to that project name.
    """
    content = (SCRIPTS_DIR / script_name).read_text(encoding="utf-8")
    assert (
        "vgnc_internal_orm" not in content
    ), f"{script_name} still references vgnc_internal_orm"
    assert (
        "vgnc-internal-orm" not in content
    ), f"{script_name} still references vgnc-internal-orm"
    assert (
        "VGNC Internal ORM" not in content
    ), f"{script_name} still references VGNC Internal ORM"


def test_bump_version_dry_run() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS_DIR / "bump_version.py"),
            "--current",
            "0.1.0",
            "--bump",
            "patch",
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    # First line of stdout must be the bumped version.
    stdout = result.stdout.strip().splitlines()
    assert stdout[0] == "0.1.1", f"Expected 0.1.1, got {stdout!r}"


def test_determine_version_bump() -> None:
    analysis = {
        "stats": {
            "total_commits": 2,
            "conventional_commits": {"feat": 1, "fix": 0},
            "breaking_changes": 0,
            "features": 1,
            "fixes": 0,
            "other_changes": 0,
        },
        "categorized_commits": {
            "features": [
                {
                    "hash": "abc12345",
                    "description": "add family repository",
                    "scope": "models",
                }
            ],
            "fixes": [],
            "breaking_changes": [],
            "other": [],
        },
        "summary": {
            "total": 2,
            "breaking": 0,
            "features": 1,
            "fixes": 0,
        },
    }
    with tempfile.NamedTemporaryFile(
        mode="w", suffix=".json", delete=False, dir=ROOT
    ) as f:
        json.dump(analysis, f)
        analysis_path = f.name

    try:
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "determine_version_bump.py"),
                analysis_path,
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert result.returncode == 0, result.stderr
        assert (
            result.stdout.strip() == "minor"
        ), f"Expected minor bump, got {result.stdout!r}"
    finally:
        os.unlink(analysis_path)


def test_analyze_commits_degrades_gracefully_without_conventional_commits() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        repo = Path(tmp_dir)
        subprocess.run(["git", "init"], cwd=repo, check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "test@example.com"],
            cwd=repo,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Test User"],
            cwd=repo,
            check=True,
            capture_output=True,
        )
        (repo / "README.md").write_text("seed\n", encoding="utf-8")
        subprocess.run(
            ["git", "add", "README.md"],
            cwd=repo,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "commit", "-m", "update readme"],
            cwd=repo,
            check=True,
            capture_output=True,
        )

        output_path = repo / "analysis.json"
        result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "analyze_commits.py"),
                "--range",
                "HEAD",
                "--output",
                str(output_path),
            ],
            cwd=repo,
            capture_output=True,
            text=True,
            check=False,
        )

        # The intelligent analyzer is an OPTIONAL enhancement that is not
        # vendored here. With no conventional commits and no intelligent
        # analyzer, analyze_commits must degrade gracefully (exit 0, warn)
        # rather than hard-fail the release pipeline.
        assert (
            result.returncode == 0
        ), f"expected graceful exit 0, got {result.returncode}: {result.stderr}"
        assert (
            "intelligent" in result.stderr.lower()
        ), f"expected a graceful-degradation warning: {result.stderr!r}"

        # And the analysis must resolve to "none" (no release), not error.
        bump_result = subprocess.run(
            [
                sys.executable,
                str(SCRIPTS_DIR / "determine_version_bump.py"),
                str(output_path),
            ],
            capture_output=True,
            text=True,
            check=False,
        )
        assert bump_result.returncode == 0, bump_result.stderr
        assert (
            bump_result.stdout.strip() == "none"
        ), f"expected 'none' bump, got {bump_result.stdout!r}"


def test_check_coverage_threshold_rejects_sub_70_percent() -> None:
    with tempfile.TemporaryDirectory() as tmp_dir:
        workdir = Path(tmp_dir)
        (workdir / "coverage.json").write_text(
            json.dumps(
                {
                    "totals": {
                        "percent_covered": 60.0,
                    }
                }
            ),
            encoding="utf-8",
        )

        result = subprocess.run(
            [sys.executable, str(SCRIPTS_DIR / "check_coverage_threshold.py")],
            cwd=workdir,
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 1
        assert "below minimum threshold" in result.stdout.lower()
