# Quality registry evidence audit

Run a deterministic, read-only audit of registry structure and test references:

```bash
python .claude/skills/quality-engineering/scripts/qe_evidence.py
python .claude/skills/quality-engineering/scripts/qe_evidence.py --json
python .claude/skills/quality-engineering/scripts/qe_evidence.py --root /path/to/Trade-Bot
```

The audit validates the registry against `config/quality_registry.schema.json`, checks duplicate IDs, test-path safety and on-disk existence (including symlink containment), resolves dependencies, and detects dependency cycles. JSON output is deterministic for stable inputs. Exit codes are 0 for a clean audit and 1 for findings.

**Evidence boundary:** a registry path is not proof that a test ran or passed. This tool does not execute commands and never upgrades a requirement status. CI run identity, command, result, and commit association remain authoritative execution evidence; Phase 5 wires the audit into CI.
