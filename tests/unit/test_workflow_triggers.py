from pathlib import Path

import pytest
import yaml

RELEASE_SCRIPT_EXPECTATIONS = {
    "analyze_commits": [
        (
            "analyze_commits.py",
            ["--range", "--output analysis.json"],
        ),
    ],
    "bump_version": [
        (
            "determine_version_bump.py",
            ["analysis.json"],
        ),
        (
            "bump_version.py",
            ["--current", "--bump"],
        ),
    ],
    "create_tag": [
        (
            "generate_release_notes.py",
            [
                "--analysis-file analysis.json",
                "--current-version",
                "--new-version",
                "--output release-notes.md",
            ],
        ),
        (
            "update_changelog.py",
            ["--version", "--release-notes-file release-notes.md"],
        ),
        (
            "update_version.py",
            ["--version"],
        ),
        (
            "update_version_references.py",
            ["--old-version", "--new-version"],
        ),
    ],
}


def load_workflow(path):
    workflow = yaml.safe_load(Path(path).read_text())
    # yaml 1.1 parses the `on:` key as bool True; normalize it back
    if True in workflow:
        workflow["on"] = workflow.pop(True)
    return workflow


def get_run_commands(job):
    return [step.get("run", "") for step in job.get("steps", []) if "run" in step]


def assert_workflow_triggers(name, workflow):
    on = workflow.get("on", {})

    # All workflows should only target main
    if "push" in on:
        assert on["push"].get("branches", []) == [
            "main"
        ], f"{name} push trigger has wrong branches"
    if "pull_request" in on:
        assert on["pull_request"].get("branches", []) == [
            "main"
        ], f"{name} PR trigger has wrong branches"

    # No workflows should reference dev/feature branches in triggers
    on_str = str(on)
    assert "dev" not in on_str, f"{name} on section contains forbidden branch reference"
    assert (
        "feature" not in on_str
    ), f"{name} on section contains forbidden branch reference"


@pytest.mark.parametrize(
    "workflow_name,expected_jobs",
    [
        ("ci", {"ci"}),
        ("coverage", {"coverage"}),
        ("docs", {"build_docs"}),
        ("development", {"lint"}),
    ],
)
def test_workflow_triggers(workflow_name, expected_jobs):
    workflow_path = f".github/workflows/{workflow_name}.yml"
    workflow = load_workflow(workflow_path)

    # Verify basic workflow structure
    assert workflow["name"].lower() == workflow_name.replace("_", " ").lower()
    assert set(workflow["jobs"].keys()) == expected_jobs

    # ci is a single matrixed job (unit + integration legs). Integration tests
    # run via testcontainers, so the workflow must NOT declare a GitHub-managed
    # postgres service (that would be dead config).
    if workflow_name == "ci":
        ci_job = workflow["jobs"]["ci"]
        assert "services" not in ci_job, (
            "ci workflow must not declare a postgres service "
            "(integration tests use testcontainers)"
        )

    # Verify all workflows have correct triggers
    assert_workflow_triggers(workflow_name, workflow)


def test_development_workflow_triggers():
    workflow_path = ".github/workflows/development.yml"
    workflow = load_workflow(workflow_path)

    # Development workflow should only run on PRs to main
    on_section = workflow.get("on", {})
    assert "push" not in on_section, "development workflow has push trigger"
    if "pull_request" in on_section:
        assert on_section["pull_request"].get("branches", []) == [
            "main"
        ], "development workflow PR trigger has wrong branches"


def test_ci_workflow_matrix():
    workflow_path = ".github/workflows/ci.yml"
    workflow = load_workflow(workflow_path)

    ci_job = workflow["jobs"]["ci"]
    matrix = ci_job.get("strategy", {}).get("matrix", {})

    assert matrix.get("include", []) == [
        {"name": "Unit tests", "matrix": "unit"},
        {"name": "Integration tests", "matrix": "integration"},
    ], "ci workflow matrix configuration incorrect"

    # Each leg must run exactly its own test type (no duplication, no cross-run).
    steps = ci_job.get("steps", [])
    unit_run = [
        s
        for s in steps
        if s.get("if", "") == "matrix.matrix == 'unit'"
        and "tests/unit" in s.get("run", "")
    ]
    integration_run = [
        s
        for s in steps
        if s.get("if", "") == "matrix.matrix == 'integration'"
        and "tests/integration" in s.get("run", "")
    ]
    assert unit_run, "ci unit leg must run pytest tests/unit"
    assert integration_run, "ci integration leg must run pytest tests/integration"


def test_coverage_workflow():
    workflow_path = ".github/workflows/coverage.yml"
    workflow = load_workflow(workflow_path)

    # Verify coverage workflow has correct structure
    assert workflow["name"] == "coverage"
    assert "coverage" in workflow["jobs"]
    steps = workflow["jobs"]["coverage"].get("steps", [])

    # The pytest+coverage run step must collect coverage over the package.
    assert any(
        "pytest --cov=src/pg_g4public_orm" in step.get("run", "") for step in steps
    ), "coverage workflow must run pytest --cov over the package"

    # The 70% gate must be enforced as its own step (not silently skipped by a
    # failing upload step placed before it).
    assert any(
        "coverage report --fail-under=70" in step.get("run", "") for step in steps
    ), "coverage workflow must enforce the --fail-under=70 threshold"

    # No `uv run codecov` step: codecov is not installed/configured, and a
    # failing upload would abort the workflow before the threshold check runs.
    assert not any(
        "codecov" in step.get("run", "") for step in steps
    ), "coverage workflow must not invoke codecov (not installed; would skip the gate)"

    assert_workflow_triggers("coverage", workflow)


def test_docs_workflow():
    workflow_path = ".github/workflows/docs.yml"
    workflow = load_workflow(workflow_path)

    assert workflow["name"] == "docs"
    assert "build_docs" in workflow["jobs"]
    steps = workflow["jobs"]["build_docs"].get("steps", [])

    assert any(
        "uv sync --group dev --extra dev" in step.get("run", "") for step in steps
    )
    assert any(
        "sphinx-build -b html . _build/html" in step.get("run", "") for step in steps
    )
    assert not any(
        step.get("uses", "").startswith("peaceiris/actions-gh-pages") for step in steps
    )

    assert_workflow_triggers("docs", workflow)


@pytest.mark.parametrize(
    "workflow_name,expected_jobs",
    [
        (
            "release",
            {
                "analyze_commits",
                "test",
                "bump_version",
                "create_tag",
                "github_release",
                "build_package",
            },
        ),
        ("pages", {"deploy_docs"}),
    ],
)
def test_main_only_workflow(workflow_name, expected_jobs):
    workflow_path = f".github/workflows/{workflow_name}.yml"
    workflow = load_workflow(workflow_path)

    assert workflow["name"] == workflow_name
    assert set(workflow["jobs"].keys()) == expected_jobs

    on_section = workflow.get("on", {})
    assert "push" in on_section
    assert on_section["push"]["branches"] == ["main"]
    assert "pull_request" not in on_section


@pytest.mark.parametrize(
    "workflow_name", ["ci", "coverage", "development", "docs", "pages", "release"]
)
def test_workflows_use_project_python_version(workflow_name):
    workflow = load_workflow(f".github/workflows/{workflow_name}.yml")

    for job in workflow.get("jobs", {}).values():
        for step in job.get("steps", []):
            if step.get("uses") == "actions/setup-python@v5":
                assert step.get("with", {}).get("python-version") == "3.13"


def test_release_workflow_concurrency_lock():
    workflow = load_workflow(".github/workflows/release.yml")

    concurrency = workflow.get("concurrency", {})
    assert concurrency.get("group") == "release-${{ github.ref }}"
    assert concurrency.get("cancel-in-progress") is False


def test_release_uses_expected_script_arguments():
    workflow = load_workflow(".github/workflows/release.yml")

    for job_name, script_requirements in RELEASE_SCRIPT_EXPECTATIONS.items():
        commands = get_run_commands(workflow["jobs"][job_name])

        for script_name, required_fragments in script_requirements:
            assert any(
                f"python .github/scripts/{script_name}" in command
                and all(fragment in command for fragment in required_fragments)
                for command in commands
            ), (
                f"{job_name} is missing expected {script_name} invocation "
                f"with fragments: {required_fragments}"
            )


def test_release_skips_tagging_when_bump_is_none():
    workflow = load_workflow(".github/workflows/release.yml")

    bump_job = workflow["jobs"]["bump_version"]
    assert (
        bump_job.get("outputs", {}).get("bump_type")
        == "${{ steps.determine.outputs.bump_type }}"
    )

    create_tag_job = workflow["jobs"]["create_tag"]
    condition = create_tag_job.get("if", "")
    assert "needs.bump_version.outputs.bump_type" in condition
    assert "!= 'none'" in condition


def test_release_commits_bump_before_tagging():
    workflow = load_workflow(".github/workflows/release.yml")
    commands = get_run_commands(workflow["jobs"]["create_tag"])

    commit_commands = [command for command in commands if "git commit -m" in command]
    assert commit_commands
    assert all("[skip ci]" not in command for command in commit_commands)
    assert any("git push origin HEAD:main" in command for command in commands)


def test_release_tag_push_is_idempotent():
    workflow = load_workflow(".github/workflows/release.yml")
    commands = get_run_commands(workflow["jobs"]["create_tag"])

    assert any(
        "git ls-remote --exit-code --tags origin" in command for command in commands
    )
    assert any(
        "git tag" in command and "git push origin" in command for command in commands
    )


def test_release_builds_distribution_from_tagged_commit():
    workflow = load_workflow(".github/workflows/release.yml")

    build_job = workflow["jobs"]["build_package"]
    assert set(build_job.get("needs", [])) == {"create_tag", "bump_version"}

    checkout_step = build_job.get("steps", [])[0]
    assert checkout_step.get("uses") == "actions/checkout@v4"
    assert (
        checkout_step.get("with", {}).get("ref")
        == "v${{ needs.bump_version.outputs.new_version }}"
    )

    steps = build_job.get("steps", [])
    assert any("uv build" in step.get("run", "") for step in steps)


def test_pages_workflow_deploys_docs():
    workflow_path = ".github/workflows/pages.yml"
    workflow = load_workflow(workflow_path)

    assert workflow["name"] == "pages"
    assert workflow.get("permissions", {}).get("contents") == "write"
    assert "deploy_docs" in workflow["jobs"]
    deploy_job = workflow["jobs"]["deploy_docs"]
    steps = deploy_job.get("steps", [])

    assert any(
        "uv sync --group dev --extra dev" in step.get("run", "") for step in steps
    )
    assert any(
        step.get("uses", "").startswith("peaceiris/actions-gh-pages") for step in steps
    )
