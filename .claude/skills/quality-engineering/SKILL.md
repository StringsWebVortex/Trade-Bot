---
name: quality-engineering
description: Use when editing src/ files, adding a regression entry to the registry, following the workflow for a defect fix or production behaviour change, or running qe_gate.py to validate a change plan.
---

Quality-engineering skill for the Trade-Bot repository.


## Change-plan contract

Before implementing a defect fix or production-behaviour change, write a JSON change plan and validate it:

```bash
python .claude/skills/quality-engineering/scripts/qe_gate.py --plan path/to/change-plan.json
```

The plan must use the Draft 7 schema at `schemas/change_plan.schema.json`. It requires a bounded summary, a declared change class, one or more requirement references, at least one decisive test with a `decides` statement, and a concrete failure mode. Optional blast-radius and rollback fields make operational impact explicit. Unknown fields and unqualified test paths are rejected.

A `defect_fix` plan must include a new `REG-NNNN` requirement. Do not claim verification merely because a test is named: the test must actually run and pass before the registry status is changed to `verified`.


## Registry evidence audit

Run the read-only traceability audit with `python .claude/skills/quality-engineering/scripts/qe_evidence.py`. It validates registry schema, unique IDs, safe and existing test paths, dependency references, and dependency cycles. The `gate-registry-evidence` gate runs the same audit as a blocking check. A passing audit proves references resolve; it does not prove the tests executed or passed. CI execution evidence remains authoritative.
