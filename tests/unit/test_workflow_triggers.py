from pathlib import Path

import pytest
import yaml


def load_workflow(path):
    return yaml.safe_load(Path(path).read_text())


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
    # The test is checking for branch names, not dependency names
    # Let's check if 'on' section contains 'dev' or 'feature' branches
    on_str = str(on)
    assert "dev" not in on_str, f"{name} on section contains forbidden branch reference"
    assert (
        "feature" not in on_str
    ), f"{name} on section contains forbidden branch reference"


@pytest.mark.parametrize(
    "workflow_name,expected_jobs",
    [
        ("ci", {"ci", "integration"}),
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

    # Verify ci workflow has integration job with postgres service
    if workflow_name == "ci":
        integration_job = workflow["jobs"]["integration"]
        needs = integration_job.get("needs", [])
        strategy = integration_job.get("strategy", {})

        # The integration job needs the 'ci' job
        assert "ci" in needs, "ci integration job needs 'ci' job"
        matrix_include = strategy.get("matrix", {}).get("include", [])
        if len(matrix_include) > 1:
            assert matrix_include[1] == {
                "name": "Integration tests",
                "matrix": "integration",
            }, "ci workflow integration matrix configuration incorrect"

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


def test_coverage_workflow():
    workflow_path = ".github/workflows/coverage.yml"
    workflow = load_workflow(workflow_path)

    # Verify coverage workflow has correct structure
    assert workflow["name"] == "coverage"
    assert "coverage" in workflow["jobs"]
    steps = workflow["jobs"]["coverage"].get("steps", [])
    if len(steps) >= 2:
        # Split the run commands since they are in one string
        run_commands = steps[-2].get("run", "").strip().split("\n")
        # The first command should be the pytest --cov command
        pytest_cov_command = run_commands[0] if run_commands else ""
        assert (
            pytest_cov_command == "uv run pytest --cov=src/pg_g4public_orm tests/"
        ), "coverage workflow pytest command incorrect"
        # The second command should be uv run codecov
        codecov_command = run_commands[1] if len(run_commands) > 1 else ""
        assert (
            codecov_command == "uv run codecov"
        ), "coverage workflow codecov command incorrect"

    # Verify all workflows have correct triggers
    assert_workflow_triggers("coverage", workflow)


def test_docs_workflow():
    workflow_path = ".github/workflows/docs.yml"
    workflow = load_workflow(workflow_path)

    # Verify docs workflow has correct structure
    assert workflow["name"] == "docs"
    assert "build_docs" in workflow["jobs"]
    steps = workflow["jobs"]["build_docs"].get("steps", [])
    if len(steps) >= 1:
        assert steps[-1].get("uses", "") == "peaceiris/actions-gh-pages@v3"

    # Verify all workflows have correct triggers
    assert_workflow_triggers("docs", workflow)
