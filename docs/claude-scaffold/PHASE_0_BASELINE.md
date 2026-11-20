# Claude scaffold baseline (Phase 0)

**Baseline commit:** `a6cb81283cad237a6f313e05dbafd2d012eb9caa`  
**Baseline branch:** `claude/project-thread-96rsrm`  
**Scope:** Claude Code orchestration, hook wiring, quality-engineering skill, and their verification contracts. This document records the repository as inspected; it is not a restoration specification.

## Existing architecture

| Layer | Current implementation | Baseline observation |
|---|---|---|
| Project instructions | `CLAUDE.md` | Documents Python/FastAPI + React/Vite layout, commands, agent roles, and QE workflow. |
| Claude settings | `.claude/settings.json` | Registers PostToolUse hooks for `post_edit_check.sh` and `quality_gate.py`. |
| Alternate hook settings | `.claude/hooks/settings.json` | Contains a separate PostToolUse configuration for `post_edit_check.py`; Claude Code does not automatically merge this file with the root settings file. |
| Hook adapters | `.claude/hooks/` | Includes post-edit, quality, pre-tool, completion, observation, lifecycle, and checkpoint scripts. |
| Agent definitions | `.claude/agents/` | Markdown agents include explorer, auditor, fixer, reviewer, editor, debugger, test-runner, context-gatherer, and async-security-reviewer. |
| QE skill | `.claude/skills/quality-engineering/` | Contains skill instructions, JSON config, schemas, and gate/registry scripts. |
| QE registry | `config/quality_registry.json` and `config/quality_registry.schema.json` | Registry data and its schema are configured by `qe.config.json`. |
| Existing verification | `tests/agent_control/` and other test suites | Existing agent-control tests cover hooks, completion, CLI, Git safety, and model behavior. |

## Confirmed baseline risks and inconsistencies

1. **Two settings files define different hook wiring.** The active project-level file is `.claude/settings.json`; `.claude/hooks/settings.json` is a separate file and should be treated as reference/configuration data unless explicitly loaded by a supported mechanism.
2. **Instruction/config drift.** `CLAUDE.md` describes the quality gate as running after every edit. The project-level settings do register `quality_gate.py`, but the quality-gate implementation must be tested for enforcement semantics separately; mere registration is not proof of enforcement.
3. **Scaffold references are not centrally validated.** Agent frontmatter, skill metadata, JSON configuration, hook command paths, and QE registry references need one deterministic repository-level contract check.
4. **QE schema strength is uneven.** `change_plan.schema.json` is currently only an object type declaration; it does not constrain plan structure. Phase 1 records this as a known gap rather than silently changing the plan contract without a design decision.
5. **Hook policy requires dedicated behavioral tests.** Hook adapters and their delegated runtime exist, but failure behavior (fail-open vs fail-closed), malformed stdin, and stop/precompact semantics need explicit tests in the subsequent hook-runtime phase.

## Project constraints

- Python requirement is `>=3.11,<3.12`; pytest is configured with strict markers/config and a 99% branch-coverage floor.
- Coverage source packages are explicitly listed in `pyproject.toml`; `scripts/` is not part of that source list.
- Backend and frontend checks are orchestrated by repository scripts; do not assume every optional tool or frontend dependency is installed in every environment.
- No Phase 0/1 change may execute exchange requests, place orders, access production credentials, mutate databases, or alter trading behavior.

## Phase 0 exit criteria

- [x] Record the actual PR head SHA and branch.
- [x] Inventory the scaffold's authoritative entry points and existing tests.
- [x] Record known wiring/schema gaps without restoring or deleting files.
- [ ] Keep the baseline document aligned with the final validator contract.
