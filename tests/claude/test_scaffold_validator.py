"""Contract tests for the Claude scaffold validator."""
from __future__ import annotations

import json
from pathlib import Path

from scripts.claude.validate_scaffold import ScaffoldValidator, find_root


def write(root: Path, relative: str, content: str) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def valid_tree(root: Path) -> None:
    for relative in (
        "CLAUDE.md",
        ".claude/hooks/post_edit_check.py",
        ".claude/skills/quality-engineering/scripts/qe_gate.py",
        ".claude/skills/quality-engineering/scripts/qe_new_requirement.py",
        "config/quality_registry.json",
        "config/quality_registry.schema.json",
        "src/quality/registry.py",
        "scripts/generate_quality_docs.py",
        "docs/quality/REQUIREMENTS_TRACEABILITY.md",
    ):
        write(root, relative, "# fixture\n")
    write(
        root,
        ".claude/settings.json",
        json.dumps({
            "hooks": {
                "PostToolUse": [{
                    "matcher": "Edit|Write",
                    "hooks": [{
                        "type": "command",
                        "command": 'python "$CLAUDE_PROJECT_DIR"/.claude/hooks/post_edit_check.py',
                    }],
                }],
            },
        }),
    )
    write(
        root,
        ".claude/agents/reviewer.md",
        "---\nname: reviewer\ndescription: Read-only review agent\ntools: Read, Grep\nmodel: sonnet\n---\nReview.\n",
    )
    write(
        root,
        ".claude/skills/quality-engineering/SKILL.md",
        "---\nname: quality-engineering\ndescription: Run quality gates\n---\nQE skill.\n",
    )
    write(
        root,
        ".claude/skills/quality-engineering/schemas/qe_config.schema.json",
        json.dumps({"$schema": "https://json-schema.org/draft/2020-12/schema", "type": "object", "required": ["version"]}),
    )
    write(
        root,
        ".claude/skills/quality-engineering/qe.config.json",
        json.dumps({
            "version": "1",
            "name": "quality-engineering",
            "gates": [{
                "id": "unit",
                "why": "Run the unit tests before completing the change.",
                "command": "python -m pytest",
                "blocking": True,
            }],
            "never": [],
            "registry": {
                "path": "config/quality_registry.json",
                "schema": "config/quality_registry.schema.json",
                "loader": "src/quality/registry.py",
                "generated_docs": [{
                    "generator": "scripts/generate_quality_docs.py",
                    "doc": "docs/quality/REQUIREMENTS_TRACEABILITY.md",
                }],
                "id_prefixes": {"REG-": "regression"},
            },
        }),
    )


def test_valid_scaffold_passes(tmp_path: Path) -> None:
    valid_tree(tmp_path)
    assert ScaffoldValidator(tmp_path).validate() == []


def test_missing_required_file_is_reported(tmp_path: Path) -> None:
    valid_tree(tmp_path)
    (tmp_path / "CLAUDE.md").unlink()
    assert any("CLAUDE.md" in item and "missing" in item for item in ScaffoldValidator(tmp_path).validate())


def test_missing_hook_target_is_reported(tmp_path: Path) -> None:
    valid_tree(tmp_path)
    (tmp_path / ".claude/hooks/post_edit_check.py").unlink()
    errors = ScaffoldValidator(tmp_path).validate()
    assert any("post_edit_check.py" in item and "does not exist" in item for item in errors)


def test_invalid_settings_json_is_reported(tmp_path: Path) -> None:
    valid_tree(tmp_path)
    write(tmp_path, ".claude/settings.json", "{")
    assert any("invalid JSON" in item for item in ScaffoldValidator(tmp_path).validate())


def test_hook_without_repo_hook_reference_is_rejected(tmp_path: Path) -> None:
    valid_tree(tmp_path)
    settings = json.loads((tmp_path / ".claude/settings.json").read_text())
    settings["hooks"]["PostToolUse"][0]["hooks"][0]["command"] = "echo unsafe"
    write(tmp_path, ".claude/settings.json", json.dumps(settings))
    assert any("must reference" in item for item in ScaffoldValidator(tmp_path).validate())


def test_agent_frontmatter_fields_are_required(tmp_path: Path) -> None:
    valid_tree(tmp_path)
    write(tmp_path, ".claude/agents/bad.md", "---\nname: bad\n---\n")
    errors = ScaffoldValidator(tmp_path).validate()
    assert any("description" in item and "required" in item for item in errors)


def test_duplicate_agent_names_are_rejected(tmp_path: Path) -> None:
    valid_tree(tmp_path)
    write(
        tmp_path,
        ".claude/agents/duplicate.md",
        "---\nname: reviewer\ndescription: Duplicate\ntools: Read\nmodel: haiku\n---\n",
    )
    assert any("duplicate agent name" in item for item in ScaffoldValidator(tmp_path).validate())


def test_duplicate_gate_ids_are_rejected(tmp_path: Path) -> None:
    valid_tree(tmp_path)
    config_path = tmp_path / ".claude/skills/quality-engineering/qe.config.json"
    config = json.loads(config_path.read_text())
    config["gates"].append(dict(config["gates"][0]))
    write(tmp_path, ".claude/skills/quality-engineering/qe.config.json", json.dumps(config))
    assert any("duplicate gate id" in item for item in ScaffoldValidator(tmp_path).validate())


def test_registry_path_traversal_is_rejected(tmp_path: Path) -> None:
    valid_tree(tmp_path)
    config_path = tmp_path / ".claude/skills/quality-engineering/qe.config.json"
    config = json.loads(config_path.read_text())
    config["registry"]["loader"] = "../outside.py"
    write(tmp_path, ".claude/skills/quality-engineering/qe.config.json", json.dumps(config))
    assert any("escapes repository root" in item for item in ScaffoldValidator(tmp_path).validate())


def test_missing_generated_document_is_rejected(tmp_path: Path) -> None:
    valid_tree(tmp_path)
    config_path = tmp_path / ".claude/skills/quality-engineering/qe.config.json"
    config = json.loads(config_path.read_text())
    config["registry"]["generated_docs"][0]["doc"] = "docs/missing.md"
    write(tmp_path, ".claude/skills/quality-engineering/qe.config.json", json.dumps(config))
    assert any("docs/missing.md" in item for item in ScaffoldValidator(tmp_path).validate())


def test_root_detection_uses_repository_markers(tmp_path: Path) -> None:
    write(tmp_path, "CLAUDE.md", "")
    write(tmp_path, ".claude/settings.json", "{}")
    write(tmp_path, "pyproject.toml", "")
    nested = tmp_path / "scripts" / "claude"
    nested.mkdir(parents=True)
    assert find_root(nested) == tmp_path


def test_validator_deduplicates_and_sorts_errors(tmp_path: Path) -> None:
    valid_tree(tmp_path)
    (tmp_path / ".claude/agents/reviewer.md").write_text("not frontmatter", encoding="utf-8")
    errors = ScaffoldValidator(tmp_path).validate()
    assert errors == sorted(set(errors))
