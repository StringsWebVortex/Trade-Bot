"""Deploy dispatch inputs never reach a shell by interpolation.

Decides:
  - SEC-1021 — Deploy dispatch inputs are never interpolated into shell
"""

from __future__ import annotations

from pathlib import Path

import yaml

WORKFLOW = Path(__file__).resolve().parents[1] / ".github" / "workflows" / "deploy.yml"


def _spec() -> dict:
    return yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))


def test_no_run_step_interpolates_an_input() -> None:
    for name, job in _spec()["jobs"].items():
        for step in job["steps"]:
            assert "${{" not in step.get("run", ""), (name, step.get("name"))


def test_artifact_run_id_is_validated_as_numeric_in_preflight() -> None:
    steps = _spec()["jobs"]["preflight"]["steps"]
    (check,) = [s for s in steps if "[0-9]+" in s.get("run", "")]
    assert check["env"]["RUN_ID"] == "${{ inputs.artifact_run_id }}"
    assert steps.index(check) < min(
        i for i, s in enumerate(steps) if "download-artifact" in s.get("uses", "")
    )
