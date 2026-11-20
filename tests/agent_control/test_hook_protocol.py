"""Tests for the Claude hook process-boundary contract."""
from __future__ import annotations

import json

import pytest

from src.agent_control.hook_protocol import (
    HOOK_SPECS,
    HookProtocolError,
    HookSpec,
    format_result,
    get_hook_spec,
    parse_event,
)


def test_registry_declares_each_supported_hook_and_wire_shape() -> None:
    assert set(HOOK_SPECS) == {"stop", "precompact", "session-start", "post-bash"}
    assert get_hook_spec("stop") == HookSpec("stop", "stop", "json")
    assert get_hook_spec("precompact").output == "json"
    assert get_hook_spec("session-start").output == "text"
    assert get_hook_spec("post-bash").output == "none"


def test_unknown_hook_is_rejected_without_key_error_leakage() -> None:
    with pytest.raises(HookProtocolError, match="unknown hook 'missing'"):
        get_hook_spec("missing")


@pytest.mark.parametrize("raw", ["", " ", "\n", "\t"])
def test_empty_stdin_is_an_empty_event(raw: str) -> None:
    assert parse_event(raw) == {}


def test_json_object_payload_is_parsed() -> None:
    assert parse_event('{"cwd":"/repo","tool_input":{"command":"git status"}}') == {
        "cwd": "/repo",
        "tool_input": {"command": "git status"},
    }


@pytest.mark.parametrize("raw", ["{broken", "{", '{"x": }'])
def test_invalid_json_is_reported_as_protocol_error(raw: str) -> None:
    with pytest.raises(HookProtocolError, match="invalid JSON payload"):
        parse_event(raw)


@pytest.mark.parametrize("raw", ['[]', 'null', '"event"', '1', 'true'])
def test_non_object_json_is_rejected(raw: str) -> None:
    with pytest.raises(HookProtocolError, match="not a JSON object"):
        parse_event(raw)


def test_json_result_is_one_json_line() -> None:
    assert format_result(get_hook_spec("stop"), {"decision": "block"}) == (
        json.dumps({"decision": "block"}) + "\n"
    )


def test_json_none_result_emits_nothing() -> None:
    assert format_result(get_hook_spec("stop"), None) is None


def test_json_result_must_be_an_object() -> None:
    with pytest.raises(HookProtocolError, match="must return an object"):
        format_result(get_hook_spec("stop"), "not-json")


def test_text_result_is_newline_terminated() -> None:
    assert format_result(get_hook_spec("session-start"), "recovered") == "recovered\n"


def test_empty_text_result_emits_nothing() -> None:
    assert format_result(get_hook_spec("session-start"), "") is None
    assert format_result(get_hook_spec("session-start"), None) is None


def test_text_result_must_be_a_string() -> None:
    with pytest.raises(HookProtocolError, match="must return text"):
        format_result(get_hook_spec("session-start"), {"unexpected": "object"})


def test_no_output_hook_accepts_only_none() -> None:
    assert format_result(get_hook_spec("post-bash"), None) is None
    with pytest.raises(HookProtocolError, match="must not return output"):
        format_result(get_hook_spec("post-bash"), "unexpected")
