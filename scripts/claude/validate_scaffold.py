#!/usr/bin/env python3
"""Validate structural contracts for the repository's Claude Code scaffold.

This command is read-only and uses only the Python standard library. It never
executes commands declared in Claude settings or QE configuration.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

REPOSITORY_MARKERS = ("CLAUDE.md", ".claude/settings.json", "pyproject.toml")
REQUIRED_FILES = (
    "CLAUDE.md",
    ".claude/settings.json",
    ".claude/skills/quality-engineering/SKILL.md",
    ".claude/skills/quality-engineering/qe.config.json",
    ".claude/skills/quality-engineering/schemas/qe_config.schema.json",
    ".claude/skills/quality-engineering/scripts/qe_gate.py",
    ".claude/skills/quality-engineering/scripts/qe_new_requirement.py",
)
HOOK_PATH_PATTERN = re.compile(r"\.claude/hooks/[A-Za-z0-9_.-]+")


class ScaffoldValidator:
    """Collect deterministic scaffold violations without mutating the tree."""

    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.errors: list[str] = []

    def error(self, location: str, message: str) -> None:
        self.errors.append(f"{location}: {message}")

    def repo_file(self, value: Any, location: str) -> Path | None:
        if not isinstance(value, str) or not value.strip():
            self.error(location, "expected a non-empty repository-relative path")
            return None
        candidate = Path(value)
        if candidate.is_absolute():
            self.error(location, f"absolute paths are forbidden: {value}")
            return None
        resolved = (self.root / candidate).resolve()
        try:
            resolved.relative_to(self.root)
        except ValueError:
            self.error(location, f"path escapes repository root: {value}")
            return None
        if not resolved.is_file():
            self.error(location, f"referenced file does not exist: {value}")
            return None
        return resolved

    def read_json(self, relative: str) -> dict[str, Any] | None:
        path = self.root / relative
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except OSError as exc:
            self.error(relative, f"cannot read file: {exc}")
            return None
        except json.JSONDecodeError as exc:
            self.error(relative, f"invalid JSON at line {exc.lineno}, column {exc.colno}")
            return None
        if not isinstance(data, dict):
            self.error(relative, "top-level JSON value must be an object")
            return None
        return data

    @staticmethod
    def frontmatter(path: Path) -> dict[str, str] | None:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            return None
        lines = text.splitlines()
        if not lines or lines[0].strip() != "---":
            return None
        try:
            end = lines.index("---", 1)
        except ValueError:
            return None
        metadata: dict[str, str] = {}
        for line in lines[1:end]:
            if not line.strip() or line.lstrip().startswith("#") or ":" not in line:
                continue
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip("'\\\"")
        return metadata

    def check_required_files(self) -> None:
        for relative in REQUIRED_FILES:
            if not (self.root / relative).is_file():
                self.error(relative, "required scaffold file is missing")
        agents = self.root / ".claude/agents"
        if not agents.is_dir() or not any(agents.glob("*.md")):
            self.error(".claude/agents", "at least one agent Markdown file is required")
        hooks = self.root / ".claude/hooks"
        if not hooks.is_dir():
            self.error(".claude/hooks", "hook directory is required")

    def check_settings(self) -> None:
        settings_path = self.root / ".claude/settings.json"
        if not settings_path.is_file():
            return
        settings = self.read_json(".claude/settings.json")
        if settings is None:
            return
        hooks = settings.get("hooks")
        if not isinstance(hooks, dict) or not hooks:
            self.error(".claude/settings.json", "hooks must be a non-empty object")
            return
        for event, matchers in hooks.items():
            location = f".claude/settings.json:hooks.{event}"
            if not isinstance(matchers, list) or not matchers:
                self.error(location, "event must contain at least one matcher")
                continue
            for index, matcher in enumerate(matchers):
                item_location = f"{location}[{index}]"
                if not isinstance(matcher, dict):
                    self.error(item_location, "matcher must be an object")
                    continue
                if not isinstance(matcher.get("matcher"), str) or not matcher["matcher"].strip():
                    self.error(item_location, "matcher must be a non-empty string")
                commands = matcher.get("hooks")
                if not isinstance(commands, list) or not commands:
                    self.error(item_location, "hooks must be a non-empty array")
                    continue
                for command_index, command in enumerate(commands):
                    command_location = f"{item_location}.hooks[{command_index}]"
                    if not isinstance(command, dict) or command.get("type") != "command":
                        self.error(command_location, 'hook must be an object with type "command"')
                        continue
                    command_text = command.get("command")
                    if not isinstance(command_text, str) or not command_text.strip():
                        self.error(command_location, "command must be a non-empty string")
                        continue
                    references = HOOK_PATH_PATTERN.findall(command_text)
                    if not references:
                        self.error(command_location, "command must reference a repository .claude/hooks file")
                    for reference in references:
                        self.repo_file(reference, command_location)

    def check_agents(self) -> None:
        directory = self.root / ".claude/agents"
        if not directory.is_dir():
            return
        seen: set[str] = set()
        for path in sorted(directory.glob("*.md")):
            relative = path.relative_to(self.root).as_posix()
            metadata = self.frontmatter(path)
            if metadata is None:
                self.error(relative, "missing or malformed YAML frontmatter")
                continue
            for field in ("name", "description", "tools", "model"):
                if not metadata.get(field, "").strip():
                    self.error(relative, f"frontmatter field {field!r} is required")
            name = metadata.get("name", "").strip()
            if name and name in seen:
                self.error(relative, f"duplicate agent name: {name}")
            seen.add(name)

    def check_skill(self) -> None:
        relative = ".claude/skills/quality-engineering/SKILL.md"
        path = self.root / relative
        if path.is_file():
            metadata = self.frontmatter(path)
            if metadata is None:
                self.error(relative, "missing or malformed YAML frontmatter")
            else:
                for field in ("name", "description"):
                    if not metadata.get(field, "").strip():
                        self.error(relative, f"frontmatter field {field!r} is required")

    def check_qe_config(self) -> None:
        config_path = ".claude/skills/quality-engineering/qe.config.json"
        schema_path = ".claude/skills/quality-engineering/schemas/qe_config.schema.json"
        config = self.read_json(config_path) if (self.root / config_path).is_file() else None
        schema = self.read_json(schema_path) if (self.root / schema_path).is_file() else None
        if schema is not None:
            if not isinstance(schema.get("$schema"), str) or not schema["$schema"]:
                self.error(schema_path, "$schema declaration is required")
            if schema.get("type") != "object":
                self.error(schema_path, 'root schema type must be "object"')
            if not isinstance(schema.get("required"), list) or not schema["required"]:
                self.error(schema_path, "root schema must declare required properties")
        if config is None:
            return
        for key in ("version", "name", "gates", "never", "registry"):
            if key not in config:
                self.error(config_path, f"required property {key!r} is missing")
        gates = config.get("gates")
        if not isinstance(gates, list):
            self.error(config_path, "gates must be an array")
            gates = []
        seen_gate_ids: set[str] = set()
        for index, gate in enumerate(gates):
            location = f"{config_path}:gates[{index}]"
            if not isinstance(gate, dict):
                self.error(location, "gate must be an object")
                continue
            gate_id = gate.get("id")
            if not isinstance(gate_id, str) or not gate_id.strip():
                self.error(location, "gate id must be a non-empty string")
            elif gate_id in seen_gate_ids:
                self.error(location, f"duplicate gate id: {gate_id}")
            else:
                seen_gate_ids.add(gate_id)
            for key in ("why", "command"):
                if not isinstance(gate.get(key), str) or not gate[key].strip():
                    self.error(location, f"{key} must be a non-empty string")
            if not isinstance(gate.get("blocking"), bool):
                self.error(location, "blocking must be a boolean")
            command = gate.get("command")
            if isinstance(command, str):
                match = re.match(r"^([A-Za-z0-9_./-]+)", command.strip())
                if match and ("/" in match.group(1) or match.group(1).endswith(".py")):
                    self.repo_file(match.group(1), f"{location}.command")
        registry = config.get("registry")
        if not isinstance(registry, dict):
            self.error(config_path, "registry must be an object")
            return
        for key in ("path", "schema", "loader"):
            self.repo_file(registry.get(key), f"{config_path}:registry.{key}")
        generated = registry.get("generated_docs")
        if not isinstance(generated, list):
            self.error(config_path, "registry.generated_docs must be an array")
        else:
            for index, item in enumerate(generated):
                location = f"{config_path}:registry.generated_docs[{index}]"
                if not isinstance(item, dict):
                    self.error(location, "entry must be an object")
                    continue
                self.repo_file(item.get("generator"), f"{location}.generator")
                self.repo_file(item.get("doc"), f"{location}.doc")
        if not isinstance(registry.get("id_prefixes"), dict) or not registry["id_prefixes"]:
            self.error(config_path, "registry.id_prefixes must be a non-empty object")

    def validate(self) -> list[str]:
        self.check_required_files()
        self.check_settings()
        self.check_agents()
        self.check_skill()
        self.check_qe_config()
        return sorted(set(self.errors))


def find_root(start: Path) -> Path | None:
    current = start.resolve()
    for candidate in (current, *current.parents):
        if all((candidate / marker).exists() for marker in REPOSITORY_MARKERS):
            return candidate
    return None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, help="repository root (auto-detected by default)")
    args = parser.parse_args(argv)
    root = args.root.resolve() if args.root else find_root(Path(__file__).parent)
    if root is None or not root.is_dir():
        print("ERROR: repository root not found; pass --root explicitly", file=sys.stderr)
        return 2
    errors = ScaffoldValidator(root).validate()
    if errors:
        print(f"Claude scaffold validation: FAIL ({len(errors)} issue(s))")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Claude scaffold validation: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
