"""Tests for orchestrator/planner.py (the new plan-big/execute-small package,
distinct from src/engine/orchestrator.py covered by tests/test_orchestrator*.py).

Decides: REG-1226"""

from __future__ import annotations

import json
from unittest.mock import patch

import pytest

from orchestrator.planner import plan


def test_plan_parses_plain_json_array():
    with patch("orchestrator.planner.run_claude", return_value={"result": '["a", "b"]'}):
        assert plan("goal") == ["a", "b"]


def test_plan_strips_fenced_code_block_with_language_tag():
    fenced = '```json\n["a", "b"]\n```'
    with patch("orchestrator.planner.run_claude", return_value={"result": fenced}):
        assert plan("goal") == ["a", "b"]


def test_plan_strips_bare_fence_no_newline():
    # "```[\"a\"]```" -> strip("`") leaves "[\"a\"]" with no "\n" to split on
    fenced = "```" + json.dumps(["a"]) + "```"
    with patch("orchestrator.planner.run_claude", return_value={"result": fenced}):
        assert plan("goal") == ["a"]


def test_plan_raises_on_non_list_response():
    with patch("orchestrator.planner.run_claude", return_value={"result": '{"not": "a list"}'}):
        with pytest.raises(ValueError, match="did not return a JSON list"):
            plan("goal")


def test_plan_truncates_to_max_subtasks():
    with (
        patch("orchestrator.planner.MAX_SUBTASKS", 2),
        patch("orchestrator.planner.run_claude", return_value={"result": '["a", "b", "c"]'}),
    ):
        assert plan("goal") == ["a", "b"]


def test_plan_prefers_structured_output():
    out = {"result": "", "structured_output": {"subtasks": ["x", "y", "z"]}}
    with (
        patch("orchestrator.planner.MAX_SUBTASKS", 2),
        patch("orchestrator.planner.run_claude", return_value=out) as run_claude,
    ):
        assert plan("goal") == ["x", "y"]
    assert run_claude.call_args.kwargs["json_schema"]["required"] == ["subtasks"]


def test_plan_tolerates_prose_around_the_json_array():
    text = 'Here you go:\n```json\n["a", "b"]\n```\nHope that helps!'
    with patch("orchestrator.planner.run_claude", return_value={"result": text}):
        assert plan("goal") == ["a", "b"]
