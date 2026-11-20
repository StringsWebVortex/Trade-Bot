# Claude scaffold contract

This contract is intentionally structural. It validates that the implemented scaffold is present and internally referenced; it does not claim that every hook enforces its intended runtime policy. Behavioral enforcement belongs to hook-runtime and QE-engine tests.

## Required repository assets

- `CLAUDE.md`
- `.claude/settings.json`
- `.claude/agents/` with at least one valid agent definition
- `.claude/hooks/`
- `.claude/skills/quality-engineering/SKILL.md`
- `.claude/skills/quality-engineering/qe.config.json`
- `.claude/skills/quality-engineering/schemas/qe_config.schema.json`
- `.claude/skills/quality-engineering/scripts/qe_gate.py`
- `.claude/skills/quality-engineering/scripts/qe_new_requirement.py`

## File contracts

### Claude settings

- Must be valid JSON with a top-level `hooks` object.
- Hook event names map to arrays of matcher objects.
- Each matcher has a non-empty `matcher` and a non-empty `hooks` array.
- Each hook has `type: "command"` and a non-empty command.
- Every referenced `.claude/hooks/<file>` path must exist in the repository.

### Agent definitions

Every `.claude/agents/*.md` file must have YAML frontmatter delimited by the first two `---` lines and non-empty `name`, `description`, `tools`, and `model` fields. Agent names must be unique.

### Quality-engineering skill

The skill must have frontmatter with non-empty `name` and `description`. Its QE config and schema must parse as JSON. The config must have the required top-level keys and unique gate IDs. Paths declared for the registry, schema, loader, generated-doc generator, generated docs, and local gate commands must resolve inside the repository and exist.

### Path safety

Paths in the QE configuration must be repository-relative. Absolute paths and paths that resolve outside the repository are rejected. Missing references are errors, not warnings.

## Invocation

```bash
python scripts/claude/validate_scaffold.py
python scripts/claude/validate_scaffold.py --root /path/to/checkout
```

Exit codes: `0` means all structural checks passed; `1` means one or more contract violations; `2` means invocation or repository-root error.

## Explicit non-goals

- Does not run hooks or shell commands declared by hooks/QE gates.
- Does not execute tests, lint, type checking, exchange/network access, or database operations.
- Does not infer that a registered hook is behaviorally effective.
- Does not validate full YAML or JSON Schema semantics; deeper schema validation is a later QE-engine responsibility.
- Does not rewrite, delete, restore, or auto-correct scaffold files.
