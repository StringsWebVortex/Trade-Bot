# File Index

Index version 1.0.1. Architecture/chunk baseline HEAD 9128e3da8b9542efef5c89706b8f2e8f3512f054; inventory hashes and line counts refreshed against the current PR worktree based on main HEAD 6232016c94db2025e9afddf4aa3e3e2331dc7b2f. Inventory includes Git-tracked application/repository paths; codebase-analysis-docs/ is always excluded to prevent self-referential hashes, and other untracked user files/build outputs are excluded. SHA8 is the first eight hexadecimal digits of SHA-256 over current working-tree bytes (modified tracked files show working-tree hashes). Binary assets have no line count. P0 marks runtime/entrypoint/policy anchors; P1 high-value source/config/docs/tests; P2 supporting/other files.

## Totals

- Tracked paths: 1280
- Python files: 1053
- P0 anchors: 58
- P1 files: 1084

## Top 50 reference files

| # | Priority | Path | Type | Lines | SHA8 | Why it matters |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | P0 | .github/workflows/ci-diagnostics.yml | YAML | 43 | 2f499a19 | SHA-bound CI diagnostics collector |
| 2 | P0 | .github/workflows/ci.yml | YAML | 415 | 2abf41de | CI jobs and gate composition |
| 3 | P0 | AGENTS.md | Markdown | 562 | 2d19c12a | Engineering workflow and safety contract |
| 4 | P0 | CLAUDE.md | Markdown | 733 | 551b491d | Architecture, quality, CI and project policy |
| 5 | P0 | Dockerfile | Other text/source | 145 | db5c42f1 | Container runtime, identity, healthcheck and entrypoint |
| 6 | P0 | Makefile | Other text/source | 45 | f5f88b46 | Developer commands governed by repository policy |
| 7 | P0 | README.md | Markdown | 471 | 9d351b5a | Purpose, usage and declared architecture |
| 8 | P0 | config/architecture_layers.json | JSON | 78 | 734d6397 | Enforced import layering |
| 9 | P0 | config/command_policy.json | JSON | 304 | a0f8c0c7 | Tool command and CI observation policy |
| 10 | P0 | config/horizons.yaml | YAML | 53 | 2ede87ec | Auxiliary prediction horizon definitions |
| 11 | P0 | config/math_registry.json | JSON | 1903 | 8fa18ffc | Mathematical object registry |
| 12 | P0 | config/quality_registry.json | JSON | 9237 | 6d076b73 | Requirements, regressions and deciding tests |
| 13 | P0 | config/risk.yaml | YAML | 26 | dd4766f8 | Horizon/intelligence risk, distinct from core Settings |
| 14 | P0 | docker-compose.yml | YAML | 82 | 80ec3eca | API/Timescale/optional-worker composition |
| 15 | P0 | docs/quality/CI_GATE_ARCHITECTURE.md | Markdown | 255 | 62e800fb | CI gates |
| 16 | P0 | docs/runtime/RUNTIME_PLATFORM.md | Markdown | 296 | 37fde0ad | Runtime control plane architecture |
| 17 | P0 | docs/security/THREAT_MODEL.md | Markdown | 341 | ab52c113 | Threat model |
| 18 | P0 | docs/terminal/ARCHITECTURE.md | Markdown | 217 | ac1b11e0 | Terminal/workspace architecture; historical baseline clearly labeled |
| 19 | P0 | frontend/package.json | JSON | 47 | d63ddf52 | Node toolchain and frontend scripts |
| 20 | P0 | frontend/src/App.jsx | React JSX | 514 | 44d9a9ec | Dashboard composition |
| 21 | P0 | frontend/src/hooks/useApi.js | JavaScript | 536 | 1f84e632 | HTTP and WebSocket client |
| 22 | P0 | frontend/src/main.jsx | React JSX | 13 | 2a4613fa | React entrypoint |
| 23 | P0 | pyproject.toml | TOML | 100 | f3afbdd8 | Python version, pytest/coverage and Ruff configuration |
| 24 | P0 | requirements-dev.txt | Text | 22 | 78da51ef | Development/test dependencies |
| 25 | P0 | requirements-optional.txt | Text | 43 | aba5af86 | Optional/lazy dependencies |
| 26 | P0 | requirements.txt | Text | 96 | d8d7f348 | Runtime Python dependency source |
| 27 | P0 | src/api/__main__.py | Python | 42 | f07796d2 | API entrypoint |
| 28 | P0 | src/api/access_control.py | Python | 84 | 263fe5ed | Permission/role definitions |
| 29 | P0 | src/api/auth.py | Python | 190 | 7b3169c1 | API key and role authentication |
| 30 | P0 | src/api/main.py | Python | 3954 | 58a7b930 | FastAPI lifecycle, REST and WebSocket routes |
| 31 | P0 | src/config.py | Python | 1492 | 170f7e9c | Primary Pydantic settings and runtime config |
| 32 | P0 | src/data/clock.py | Python | 125 | 768bcae5 | UTC and venue clock helpers |
| 33 | P0 | src/data/fetcher.py | Python | 1294 | 0e7e3975 | CCXT data, retries, orderbook, reconnect |
| 34 | P0 | src/data/storage.py | Python | 2208 | 97ab6842 | SQLite backend, schema and migrations |
| 35 | P0 | src/data/timescale_storage.py | Python | 1625 | 9c8602f2 | Timescale backend |
| 36 | P0 | src/engine/orchestrator.py | Python | 3594 | 464d64eb | Main trading loop, tick, portfolio, retrain and position monitor |
| 37 | P0 | src/engine/signal_engine.py | Python | 1920 | a05db8db | Per-timeframe signal computation |
| 38 | P0 | src/execution/live.py | Python | 1643 | ccb718ba | Live executor boundary |
| 39 | P0 | src/execution/order_fsm.py | Python | 375 | 14f635a5 | Order state machine and fill aggregation |
| 40 | P0 | src/execution/unified_ledger.py | Python | 89 | 86392a2d | Cross-venue book ledger |
| 41 | P0 | src/features/pipeline.py | Python | 1250 | 5ca56a6f | Features, labels and train/inference alignment |
| 42 | P0 | src/intelligence/client.py | Python | 706 | e799d7be | Provider aggregator and caches |
| 43 | P0 | src/models/model_registry.py | Python | 173 | 96ae8c96 | Model bundle and promotion |
| 44 | P0 | src/models/online_trainer.py | Python | 377 | e55987c8 | Online prediction/outcome learning |
| 45 | P0 | src/models/trainer.py | Python | 1781 | c0be7036 | Training, CPCV/OOS metrics and artifact validation |
| 46 | P0 | src/regime/detector.py | Python | 828 | 4ca13328 | HMM regime detector |
| 47 | P0 | src/risk/gates.py | Python | 1296 | 22e195c5 | Sequential trading gates and exits |
| 48 | P0 | src/runtime/changes.py | Python | 783 | 310891d5 | Runtime change lifecycle and audit |
| 49 | P0 | src/runtime/contracts.py | Python | 504 | ad764291 | Runtime state/action/capability contracts |
| 50 | P0 | src/runtime/platform.py | Python | 145 | 1c7162da | Runtime composition root |

## Complete tracked-file index

| # | Priority | Path | Type | Lines | SHA8 | Notes |
| ---: | --- | --- | --- | ---: | --- | --- |
| 1 | P0 | .github/workflows/ci.yml | YAML | 415 | 2abf41de | CI jobs and gate composition |
| 2 | P0 | AGENTS.md | Markdown | 562 | 2d19c12a | Engineering workflow and safety contract |
| 3 | P0 | CLAUDE.md | Markdown | 733 | 551b491d | Architecture, quality, CI and project policy |
| 4 | P0 | Dockerfile | Other text/source | 145 | db5c42f1 | Container runtime, identity, healthcheck and entrypoint |
| 5 | P0 | Makefile | Other text/source | 45 | f5f88b46 | Developer commands governed by repository policy |
| 6 | P0 | README.md | Markdown | 471 | 9d351b5a | Purpose, usage and declared architecture |
| 7 | P0 | config/architecture_layers.json | JSON | 78 | 734d6397 | Enforced import layering |
| 8 | P0 | config/command_policy.json | JSON | 304 | a0f8c0c7 | Tool command and CI observation policy |
| 9 | P0 | config/horizons.yaml | YAML | 53 | 2ede87ec | Auxiliary prediction horizon definitions |
| 10 | P0 | config/math_registry.json | JSON | 1903 | 8fa18ffc | Mathematical object registry |
| 11 | P0 | config/quality_registry.json | JSON | 9237 | 6d076b73 | Requirements, regressions and deciding tests |
| 12 | P0 | config/risk.yaml | YAML | 26 | dd4766f8 | Horizon/intelligence risk, distinct from core Settings |
| 13 | P0 | docker-compose.yml | YAML | 82 | 80ec3eca | API/Timescale/optional-worker composition |
| 14 | P0 | docs/quality/CI_GATE_ARCHITECTURE.md | Markdown | 255 | 62e800fb | CI gates |
| 15 | P0 | docs/runtime/RUNTIME_PLATFORM.md | Markdown | 296 | 37fde0ad | Runtime control plane architecture |
| 16 | P0 | docs/security/THREAT_MODEL.md | Markdown | 341 | ab52c113 | Threat model |
| 17 | P0 | docs/terminal/ARCHITECTURE.md | Markdown | 217 | ac1b11e0 | Terminal/workspace architecture; historical baseline clearly labeled |
| 18 | P0 | frontend/package.json | JSON | 47 | d63ddf52 | Node toolchain and frontend scripts |
| 19 | P0 | frontend/src/App.jsx | React JSX | 514 | 44d9a9ec | Dashboard composition |
| 20 | P0 | frontend/src/hooks/useApi.js | JavaScript | 536 | 1f84e632 | HTTP and WebSocket client |
| 21 | P0 | frontend/src/main.jsx | React JSX | 13 | 2a4613fa | React entrypoint |
| 22 | P0 | pyproject.toml | TOML | 100 | f3afbdd8 | Python version, pytest/coverage and Ruff configuration |
| 23 | P0 | requirements-dev.txt | Text | 22 | 78da51ef | Development/test dependencies |
| 24 | P0 | requirements-optional.txt | Text | 43 | aba5af86 | Optional/lazy dependencies |
| 25 | P0 | requirements.txt | Text | 96 | d8d7f348 | Runtime Python dependency source |
| 26 | P0 | src/api/__main__.py | Python | 42 | f07796d2 | API entrypoint |
| 27 | P0 | src/api/access_control.py | Python | 84 | 263fe5ed | Permission/role definitions |
| 28 | P0 | src/api/auth.py | Python | 190 | 7b3169c1 | API key and role authentication |
| 29 | P0 | src/api/main.py | Python | 3954 | 58a7b930 | FastAPI lifecycle, REST and WebSocket routes |
| 30 | P0 | src/config.py | Python | 1492 | 170f7e9c | Primary Pydantic settings and runtime config |
| 31 | P0 | src/data/clock.py | Python | 125 | 768bcae5 | UTC and venue clock helpers |
| 32 | P0 | src/data/fetcher.py | Python | 1294 | 0e7e3975 | CCXT data, retries, orderbook, reconnect |
| 33 | P0 | src/data/storage.py | Python | 2208 | 97ab6842 | SQLite backend, schema and migrations |
| 34 | P0 | src/data/timescale_storage.py | Python | 1625 | 9c8602f2 | Timescale backend |
| 35 | P0 | src/engine/orchestrator.py | Python | 3594 | 464d64eb | Main trading loop, tick, portfolio, retrain and position monitor |
| 36 | P0 | src/engine/signal_engine.py | Python | 1920 | a05db8db | Per-timeframe signal computation |
| 37 | P0 | src/execution/live.py | Python | 1643 | ccb718ba | Live executor boundary |
| 38 | P0 | src/execution/order_fsm.py | Python | 375 | 14f635a5 | Order state machine and fill aggregation |
| 39 | P0 | src/execution/unified_ledger.py | Python | 89 | 86392a2d | Cross-venue book ledger |
| 40 | P0 | src/features/pipeline.py | Python | 1250 | 5ca56a6f | Features, labels and train/inference alignment |
| 41 | P0 | src/intelligence/client.py | Python | 706 | e799d7be | Provider aggregator and caches |
| 42 | P0 | src/models/model_registry.py | Python | 173 | 96ae8c96 | Model bundle and promotion |
| 43 | P0 | src/models/online_trainer.py | Python | 377 | e55987c8 | Online prediction/outcome learning |
| 44 | P0 | src/models/trainer.py | Python | 1781 | c0be7036 | Training, CPCV/OOS metrics and artifact validation |
| 45 | P0 | src/regime/detector.py | Python | 828 | 4ca13328 | HMM regime detector |
| 46 | P0 | src/risk/gates.py | Python | 1296 | 22e195c5 | Sequential trading gates and exits |
| 47 | P0 | src/runtime/changes.py | Python | 783 | 310891d5 | Runtime change lifecycle and audit |
| 48 | P0 | src/runtime/contracts.py | Python | 504 | ad764291 | Runtime state/action/capability contracts |
| 49 | P0 | src/runtime/platform.py | Python | 145 | 1c7162da | Runtime composition root |
| 50 | P0 | src/runtime/production.py | Python | 418 | 55696d76 | Production discovery/controllers/reconciliation |
| 51 | P0 | src/strategies/bootstrap.py | Python | 205 | 7c5e2f94 | Config-enabled strategy registration |
| 52 | P0 | src/strategies/registry.py | Python | 143 | 5ef08896 | Strategy protocol and ID registry |
| 53 | P0 | src/terminal/protocol.py | Python | 216 | ed293ffb | Terminal protocol validation |
| 54 | P0 | src/terminal/server.py | Python | 647 | e6fa9e24 | PTY terminal daemon |
| 55 | P0 | src/tuning/scheduler.py | Python | 712 | 93bd994d | Optional tuning scheduler |
| 56 | P0 | src/workers/orchestrator.py | Python | 871 | 152c9c6c | Horizon and ECC worker orchestration |
| 57 | P0 | src/workers/trader.py | Python | 144 | b63ee6b6 | Headless main trading loop |
| 58 | P0 | tests/test_engine_seam_contract.py | Python | 205 | fd684c46 | Positional E-01…E-18 contract test |
| 59 | P1 | .github/CODEOWNERS | Other text/source | 18 | 7fd71f34 |  |
| 60 | P1 | .github/ISSUE_TEMPLATE/bug_report.md | Markdown | 17 | 12f0ae93 |  |
| 61 | P1 | .github/ISSUE_TEMPLATE/config.yml | YAML | 5 | cf84e847 |  |
| 62 | P1 | .github/ISSUE_TEMPLATE/feature_request.md | Markdown | 15 | 68399f6b |  |
| 63 | P1 | .github/dependabot.yml | YAML | 67 | bef3b14e |  |
| 64 | P1 | .github/mermaid-puppeteer-config.json | JSON | 6 | c73c7331 |  |
| 65 | P1 | .github/pull_request_template.md | Markdown | 15 | e8ad60ce |  |
| 66 | P1 | .github/rulesets/main-protection.json | JSON | 110 | 585c7190 |  |
| 67 | P1 | .github/workflows/ci-diagnostics.yml | YAML | 43 | 2f499a19 |  |
| 68 | P1 | .github/workflows/codeql.yml | YAML | 118 | 92cec6ba |  |
| 69 | P1 | .github/workflows/codex-pr-handoff.yml | YAML | 76 | 7810b996 |  |
| 70 | P1 | .github/workflows/deploy.yml | YAML | 187 | e32b046a |  |
| 71 | P1 | .github/workflows/nightly-quality.yml | YAML | 141 | 08f2db1b |  |
| 72 | P1 | .github/workflows/pr-auto-update.yml | YAML | 328 | c6032fae |  |
| 73 | P1 | .github/workflows/rag-ingest.yml | YAML | 54 | 3ef87ddd |  |
| 74 | P1 | .github/workflows/release.yml | YAML | 133 | b595cd54 |  |
| 75 | P1 | .github/workflows/security.yml | YAML | 490 | 0d555204 |  |
| 76 | P1 | .github/workflows/workflow-lint.yml | YAML | 112 | efae0a17 |  |
| 77 | P1 | config/arch_baseline.json | JSON | 74 | 706d8223 |  |
| 78 | P1 | config/exchange_key_posture.json | JSON | 23 | eed97927 |  |
| 79 | P1 | config/intelligence.yaml | YAML | 24 | 19139199 |  |
| 80 | P1 | config/math_registry.schema.json | JSON | 250 | 0c6cac56 |  |
| 81 | P1 | config/mutation_thresholds.json | JSON | 53 | 6b50a258 |  |
| 82 | P1 | config/observation_boundary.json | JSON | 103 | ee3b28e7 |  |
| 83 | P1 | config/performance_baselines.json | JSON | 69 | 86112a85 |  |
| 84 | P1 | config/quality_registry.d/REG-1708.json | JSON | 23 | ae70eab8 |  |
| 85 | P1 | config/quality_registry.schema.json | JSON | 265 | 0cb44223 |  |
| 86 | P1 | deploy/alerts.yml | YAML | 70 | 03b321d7 |  |
| 87 | P1 | deploy/prometheus.yml | YAML | 31 | 1bfcc7dc |  |
| 88 | P1 | deploy/systemd/tradebot-api.service | Other text/source | 39 | e87631ec |  |
| 89 | P1 | deploy/systemd/tradebot-worker.service | Other text/source | 36 | 792418f8 |  |
| 90 | P1 | docs/ARCHITECTURE_GOVERNANCE.md | Markdown | 85 | fbcf4f70 |  |
| 91 | P1 | docs/CI_FAILURE_AUDIT.md | Markdown | 196 | cb35b2ea |  |
| 92 | P1 | docs/CLOUD_REVIEW.md | Markdown | 80 | a6658509 |  |
| 93 | P1 | docs/KNOWLEDGE_GRAPH.md | Markdown | 53 | 25966977 |  |
| 94 | P1 | docs/MATH_ARCHITECTURE.md | Markdown | 579 | 3cb282f8 |  |
| 95 | P1 | docs/MATH_FOUNDATIONS.md | Markdown | 800 | dfbc32dd |  |
| 96 | P1 | docs/MATH_ROADMAP.md | Markdown | 239 | 3780b490 |  |
| 97 | P1 | docs/ORCHESTRATOR.md | Markdown | 11 | e73c0c57 |  |
| 98 | P1 | docs/PTC_PATTERN.md | Markdown | 9 | 15fad706 |  |
| 99 | P1 | docs/Quality-Engineering | Other text/source | 3154 | bcb840bb |  |
| 100 | P1 | docs/REQUIRED_CHECKS.md | Markdown | 197 | 52ecdf75 |  |
| 101 | P1 | docs/SCHEMA.md | Markdown | 172 | 38bde920 |  |
| 102 | P1 | docs/adaptive_horizon_gap_list.md | Markdown | 150 | 0e6ad4f9 |  |
| 103 | P1 | docs/agent/AGENT_EXECUTION_PROTOCOL.md | Markdown | 202 | 8941b4d5 |  |
| 104 | P1 | docs/agent/AGENT_RELIABILITY.md | Markdown | 18 | 6534cb22 |  |
| 105 | P1 | docs/agents/CODEX_SETUP.md | Markdown | 41 | e3485b59 |  |
| 106 | P1 | docs/operations/DISASTER_RECOVERY.md | Markdown | 136 | 42fa88fb |  |
| 107 | P1 | docs/ops/COMPLIANCE_CHECKLIST.md | Markdown | 65 | 73c203ea |  |
| 108 | P1 | docs/ops/KEY_ROTATION.md | Markdown | 52 | 79a54c49 |  |
| 109 | P1 | docs/ops/LIVE_PROMOTION_CHECKLIST.md | Markdown | 77 | 57d72ca9 |  |
| 110 | P1 | docs/ops/REALTIME_GUI_PLAN.md | Markdown | 73 | f042d814 |  |
| 111 | P1 | docs/ops/RUNBOOK.md | Markdown | 95 | 210bbb06 |  |
| 112 | P1 | docs/quality/IMPLEMENTATION_PLAN.md | Markdown | 214 | cfd7fbbd |  |
| 113 | P1 | docs/quality/MONEY_AND_TIME.md | Markdown | 147 | 688cc8a3 |  |
| 114 | P1 | docs/quality/PRODUCTION_READINESS.md | Markdown | 112 | da760303 |  |
| 115 | P1 | docs/quality/QUALITY_BASELINE.md | Markdown | 125 | bbc75e22 |  |
| 116 | P1 | docs/quality/QUALITY_METRICS.md | Markdown | 122 | 386b71a5 |  |
| 117 | P1 | docs/quality/QUALITY_POLICY.md | Markdown | 232 | 8c4629b8 |  |
| 118 | P1 | docs/quality/REQUIREMENTS_TRACEABILITY.md | Markdown | 4915 | 77d07f02 |  |
| 119 | P1 | docs/quality/ROOT_CAUSE_TEMPLATE.md | Markdown | 84 | a55b20e9 |  |
| 120 | P1 | docs/quality/TEST_STRATEGY.md | Markdown | 252 | efbde1ba |  |
| 121 | P1 | docs/runtime/IMPLEMENTATION_MATRIX.md | Markdown | 79 | 7e5cd563 |  |
| 122 | P1 | docs/runtime/INTEGRATION_AUDIT.md | Markdown | 165 | 4ad935f9 |  |
| 123 | P1 | docs/security/GITHUB_SECURITY_CHECKLIST.md | Markdown | 191 | 84971b8c |  |
| 124 | P1 | docs/security/INCIDENT_RESPONSE.md | Markdown | 167 | 938e0757 |  |
| 125 | P1 | docs/security/KEY_MANAGEMENT.md | Markdown | 210 | cc3a60ea |  |
| 126 | P1 | docs/security/SECURITY_POLICY.md | Markdown | 361 | 4d750b78 |  |
| 127 | P1 | docs/security/claude-cloud-github-only.md | Markdown | 41 | de2c0e75 |  |
| 128 | P1 | docs/terminal/OPERATIONS.md | Markdown | 204 | f1b999ca |  |
| 129 | P1 | frontend/src/components/Controls.jsx | React JSX | 183 | 315bb378 |  |
| 130 | P1 | frontend/src/components/Panel.jsx | React JSX | 111 | 2477557c |  |
| 131 | P1 | frontend/src/components/StartupBanner.jsx | React JSX | 58 | 60b03901 |  |
| 132 | P1 | frontend/src/components/StartupBanner.test.jsx | React JSX | 66 | ff10b727 |  |
| 133 | P1 | frontend/src/components/panels/ApprovalsPanel.jsx | React JSX | 54 | 48c2aa54 |  |
| 134 | P1 | frontend/src/components/panels/ConfigPanel.jsx | React JSX | 44 | e18dafd9 |  |
| 135 | P1 | frontend/src/components/panels/ControlHubPanel.jsx | React JSX | 296 | bc07f39f |  |
| 136 | P1 | frontend/src/components/panels/EquityChart.jsx | React JSX | 102 | a31e7cea |  |
| 137 | P1 | frontend/src/components/panels/HorizonsPanel.jsx | React JSX | 143 | 403f4ef9 |  |
| 138 | P1 | frontend/src/components/panels/MonitoringPanel.jsx | React JSX | 314 | ebe53364 |  |
| 139 | P1 | frontend/src/components/panels/OperationsPanel.jsx | React JSX | 253 | 2c3383a0 |  |
| 140 | P1 | frontend/src/components/panels/PositionsPanel.jsx | React JSX | 47 | 202c0d59 |  |
| 141 | P1 | frontend/src/components/panels/RiskControlsPanel.jsx | React JSX | 82 | 1195487e |  |
| 142 | P1 | frontend/src/components/panels/RuntimePanel.jsx | React JSX | 263 | cb6c2ead |  |
| 143 | P1 | frontend/src/components/panels/SelfTuningPanel.jsx | React JSX | 95 | 557e223c |  |
| 144 | P1 | frontend/src/components/panels/StrategiesPanel.jsx | React JSX | 153 | 7e2040f5 |  |
| 145 | P1 | frontend/src/components/panels/TradesPanel.jsx | React JSX | 99 | 5004c345 |  |
| 146 | P1 | frontend/src/components/panels/VenuesPanel.jsx | React JSX | 149 | 1bf23f04 |  |
| 147 | P1 | frontend/src/components/panels/VenuesPanel.test.jsx | React JSX | 178 | c9b499e7 |  |
| 148 | P1 | frontend/src/components/panels/runtimeModel.js | JavaScript | 123 | 08bc12ef |  |
| 149 | P1 | frontend/src/components/panels/runtimeModel.test.js | JavaScript | 158 | 73ffd2cc |  |
| 150 | P1 | frontend/src/components/terminal/ProcessCenter.jsx | React JSX | 203 | f65bdaf7 |  |
| 151 | P1 | frontend/src/components/terminal/StatusBar.jsx | React JSX | 84 | aa7934c3 |  |
| 152 | P1 | frontend/src/components/terminal/TerminalDock.jsx | React JSX | 278 | de57d2d0 |  |
| 153 | P1 | frontend/src/components/terminal/XtermView.jsx | React JSX | 100 | 7249e029 |  |
| 154 | P1 | frontend/src/components/terminal/terminalUi.test.jsx | React JSX | 520 | cacf81cd |  |
| 155 | P1 | frontend/src/components/workspace/Workspace.grid.test.jsx | React JSX | 273 | ad4593c3 |  |
| 156 | P1 | frontend/src/components/workspace/Workspace.jsx | React JSX | 119 | e63a327a |  |
| 157 | P1 | frontend/src/components/workspace/Workspace.test.jsx | React JSX | 206 | 28440fb7 |  |
| 158 | P1 | frontend/src/desktop/terminalBridge.test.js | JavaScript | 328 | d102da2d |  |
| 159 | P1 | frontend/src/hooks/useApi.test.js | JavaScript | 442 | 1a2ca76f |  |
| 160 | P1 | frontend/src/index.css | CSS | 949 | 0d23705b |  |
| 161 | P1 | frontend/src/terminal/TerminalContext.jsx | React JSX | 234 | c43cd897 |  |
| 162 | P1 | frontend/src/terminal/client.js | JavaScript | 326 | 97805d86 |  |
| 163 | P1 | frontend/src/terminal/client.test.js | JavaScript | 391 | bcef5337 |  |
| 164 | P1 | frontend/src/utils/format.js | JavaScript | 36 | 889e225a |  |
| 165 | P1 | frontend/src/workspace/items.js | JavaScript | 30 | ae2ba77e |  |
| 166 | P1 | frontend/src/workspace/layoutStore.js | JavaScript | 243 | 282ceb0b |  |
| 167 | P1 | frontend/src/workspace/layoutStore.test.js | JavaScript | 348 | 8ca1d8f3 |  |
| 168 | P1 | scripts/agent_control.py | Python | 23 | ea56814d |  |
| 169 | P1 | scripts/apply_ci_patch.py | Python | 314 | 04ed146c |  |
| 170 | P1 | scripts/apply_repo_ruleset.py | Python | 271 | f09a76cc |  |
| 171 | P1 | scripts/arch_gate.sh | Shell | 94 | fc5f6d7c |  |
| 172 | P1 | scripts/assert_jobs_green.py | Python | 150 | 831ced49 |  |
| 173 | P1 | scripts/backfill.py | Python | 130 | 664b08bf |  |
| 174 | P1 | scripts/check_coverage_floors.py | Python | 119 | 8fa19e9b |  |
| 175 | P1 | scripts/check_model_artifacts.py | Python | 67 | 7c968827 |  |
| 176 | P1 | scripts/check_mutation_score.py | Python | 205 | 1f5eb926 |  |
| 177 | P1 | scripts/check_production_readiness.py | Python | 178 | 6c642773 |  |
| 178 | P1 | scripts/check_static_invariants.py | Python | 1875 | 3324fc76 |  |
| 179 | P1 | scripts/check_supply_chain.py | Python | 367 | 02350a53 |  |
| 180 | P1 | scripts/ci_diagnostics.py | Python | 1350 | 20e02745 |  |
| 181 | P1 | scripts/ci_verdict.py | Python | 43 | ede141de |  |
| 182 | P1 | scripts/codebase_knowledge_index.py | Python | 418 | 26090ac2 |  |
| 183 | P1 | scripts/codex_pr_handoff.py | Python | 227 | ceffaa47 |  |
| 184 | P1 | scripts/codex_setup.sh | Shell | 13 | 924229a8 |  |
| 185 | P1 | scripts/collect_quality_metrics.py | Python | 217 | 43f2c6af |  |
| 186 | P1 | scripts/generate_math_docs.py | Python | 237 | 588d286e |  |
| 187 | P1 | scripts/generate_quality_docs.py | Python | 258 | 16dad626 |  |
| 188 | P1 | scripts/generate_signal_fixtures.py | Python | 89 | 4323a5f5 |  |
| 189 | P1 | scripts/ingest_kg_repo.py | Python | 111 | bb5283cd |  |
| 190 | P1 | scripts/ingest_missing.py | Python | 72 | b4ed4495 |  |
| 191 | P1 | scripts/ingest_repo.py | Python | 123 | 2e2b64e3 |  |
| 192 | P1 | scripts/install_push_wait_hook.sh | Shell | 16 | 7c2d0d6b |  |
| 193 | P1 | scripts/local_checks.py | Python | 41 | 51b52a6b |  |
| 194 | P1 | scripts/npm_audit_verdict.py | Python | 313 | 099c28f4 |  |
| 195 | P1 | scripts/orchestration_template.py | Python | 81 | 592c1ba9 |  |
| 196 | P1 | scripts/prfail | Other text/source | 8 | a7a3374f |  |
| 197 | P1 | scripts/push_wait.py | Python | 361 | 83146728 |  |
| 198 | P1 | scripts/rag_smoke.py | Python | 76 | 409e0d0d |  |
| 199 | P1 | scripts/resolve_registry_merge.py | Python | 128 | 22fde313 |  |
| 200 | P1 | scripts/startup_preflight.py | Python | 605 | 8add17aa |  |
| 201 | P1 | scripts/timescaledb.sh | Shell | 115 | b847722f |  |
| 202 | P1 | scripts/write_provenance.py | Python | 172 | 0f8c8cdd |  |
| 203 | P1 | src/__init__.py | Python | 1 | 01ba4719 |  |
| 204 | P1 | src/agent_control/__init__.py | Python | 33 | c4fc322b |  |
| 205 | P1 | src/agent_control/branch_audit.py | Python | 373 | 682c7b6a |  |
| 206 | P1 | src/agent_control/cli.py | Python | 500 | 4995ee3c |  |
| 207 | P1 | src/agent_control/completion.py | Python | 236 | 0190908a |  |
| 208 | P1 | src/agent_control/git_safety.py | Python | 469 | c4c95261 |  |
| 209 | P1 | src/agent_control/gitstate.py | Python | 311 | cd4f8ff9 |  |
| 210 | P1 | src/agent_control/hooks.py | Python | 186 | d0297aad |  |
| 211 | P1 | src/agent_control/model.py | Python | 654 | ff6d3393 |  |
| 212 | P1 | src/agent_control/reliability.py | Python | 347 | 41701a53 |  |
| 213 | P1 | src/agent_control/store.py | Python | 152 | 4fac49db |  |
| 214 | P1 | src/agent_control/workspace.py | Python | 730 | 9b88866f |  |
| 215 | P1 | src/api/__init__.py | Python | 1 | 01ba4719 |  |
| 216 | P1 | src/api/control_surface.py | Python | 588 | fd3a7aea |  |
| 217 | P1 | src/api/error_hygiene.py | Python | 191 | e525a93b |  |
| 218 | P1 | src/api/fail_closed.py | Python | 144 | 8c661a47 |  |
| 219 | P1 | src/api/middleware.py | Python | 53 | 46c6392c |  |
| 220 | P1 | src/api/object_refs.py | Python | 118 | fd35ed74 |  |
| 221 | P1 | src/api/operator_secret.py | Python | 58 | 8a2c0862 |  |
| 222 | P1 | src/api/readiness.py | Python | 137 | bc260008 |  |
| 223 | P1 | src/api/runtime_control.py | Python | 325 | 15f8de40 |  |
| 224 | P1 | src/api/security_headers.py | Python | 119 | d65ab5d5 |  |
| 225 | P1 | src/api/ws_guard.py | Python | 182 | 2355808a |  |
| 226 | P1 | src/causal/__init__.py | Python | 1 | e9a9d97f |  |
| 227 | P1 | src/causal/asset_gnn.py | Python | 239 | 12712e95 |  |
| 228 | P1 | src/causal/dowhy_scm.py | Python | 151 | f070e580 |  |
| 229 | P1 | src/causal/granger.py | Python | 153 | 9ea0517d |  |
| 230 | P1 | src/data/__init__.py | Python | 1 | 01ba4719 |  |
| 231 | P1 | src/data/block_height_provider.py | Python | 69 | b283dd39 |  |
| 232 | P1 | src/data/deribit_provider.py | Python | 138 | c84580bb |  |
| 233 | P1 | src/data/duckdb_store.py | Python | 188 | ffa0a16c |  |
| 234 | P1 | src/data/exchange_flow_provider.py | Python | 143 | 507e5b4c |  |
| 235 | P1 | src/data/feeds.py | Python | 170 | e428e67b |  |
| 236 | P1 | src/data/macro_provider.py | Python | 121 | 1ae5a9dd |  |
| 237 | P1 | src/data/orderbook_stream.py | Python | 290 | 957a507c |  |
| 238 | P1 | src/data/provider_cache.py | Python | 96 | 71eedd48 |  |
| 239 | P1 | src/data/quality_gate.py | Python | 488 | 599a18aa |  |
| 240 | P1 | src/data/sentiment_provider.py | Python | 181 | fd7e70b8 |  |
| 241 | P1 | src/diagnostics/__init__.py | Python | 0 | e3b0c442 |  |
| 242 | P1 | src/diagnostics/attribution.py | Python | 274 | 64391b74 |  |
| 243 | P1 | src/diagnostics/audit_trail.py | Python | 193 | f890e29c |  |
| 244 | P1 | src/diagnostics/behavioural_guard.py | Python | 177 | 08a77c56 |  |
| 245 | P1 | src/diagnostics/decision_log_writer.py | Python | 65 | 27b315d9 |  |
| 246 | P1 | src/diagnostics/decision_trace.py | Python | 170 | 5a492736 |  |
| 247 | P1 | src/diagnostics/disaster_recovery.py | Python | 91 | 54f9957e |  |
| 248 | P1 | src/diagnostics/failsafe_policy.py | Python | 241 | 6e4d0912 |  |
| 249 | P1 | src/diagnostics/halt_triggers.py | Python | 228 | de941e38 |  |
| 250 | P1 | src/diagnostics/instrumentation.py | Python | 178 | bd148cee |  |
| 251 | P1 | src/diagnostics/metrics.py | Python | 243 | 08c13694 |  |
| 252 | P1 | src/diagnostics/performance_baseline.py | Python | 215 | 3d567cf7 |  |
| 253 | P1 | src/diagnostics/recovery_objectives.py | Python | 208 | 826b2e23 |  |
| 254 | P1 | src/diagnostics/runtime_monitor.py | Python | 454 | 48f770a4 |  |
| 255 | P1 | src/diagnostics/signal_debugger.py | Python | 605 | 7d7ad6dc |  |
| 256 | P1 | src/diagnostics/startup_selftest.py | Python | 275 | 0843ed78 |  |
| 257 | P1 | src/diagnostics/trade_auditor.py | Python | 291 | ed1d4d14 |  |
| 258 | P1 | src/diagnostics/trade_journal.py | Python | 300 | 587984e7 |  |
| 259 | P1 | src/ecc/__init__.py | Python | 7 | 3a876b3e |  |
| 260 | P1 | src/ecc/ecdsa_scan.py | Python | 276 | 8ce33648 |  |
| 261 | P1 | src/ecc/schnorr_taproot.py | Python | 176 | 87f5e5aa |  |
| 262 | P1 | src/ecc/secp256k1_cluster.py | Python | 243 | 6ac11b95 |  |
| 263 | P1 | src/ecc/utxo_curve.py | Python | 133 | 6a49ed41 |  |
| 264 | P1 | src/ecc/zksnark_detect.py | Python | 233 | 4027603d |  |
| 265 | P1 | src/engine/__init__.py | Python | 1 | 01ba4719 |  |
| 266 | P1 | src/engine/crypto_box_adapter.py | Python | 72 | 7189101b |  |
| 267 | P1 | src/engine/strategy_portfolio.py | Python | 755 | 18445303 |  |
| 268 | P1 | src/engine/universe_returns.py | Python | 318 | b7ecd613 |  |
| 269 | P1 | src/engines/__init__.py | Python | 7 | 2334de46 |  |
| 270 | P1 | src/engines/consensus.py | Python | 473 | 3df6652b |  |
| 271 | P1 | src/engines/e01_statistical.py | Python | 106 | f7a2ddb9 |  |
| 272 | P1 | src/engines/e02_microstructure.py | Python | 83 | 9d5ca1c3 |  |
| 273 | P1 | src/engines/e03_information_theory.py | Python | 133 | 6964c9f3 |  |
| 274 | P1 | src/engines/e04_fourier.py | Python | 107 | a67b15c4 |  |
| 275 | P1 | src/engines/e05_onchain.py | Python | 81 | 812837cf |  |
| 276 | P1 | src/engines/e06_fractal.py | Python | 114 | ae38ec5b |  |
| 277 | P1 | src/engines/e07_linear_algebra.py | Python | 118 | 4ab056cd |  |
| 278 | P1 | src/engines/e08_topology.py | Python | 138 | d609acdd |  |
| 279 | P1 | src/engines/e09_ml_meta.py | Python | 117 | 8a68501b |  |
| 280 | P1 | src/engines/e10_supply.py | Python | 210 | 53c6a665 |  |
| 281 | P1 | src/engines/e11_stochastic.py | Python | 120 | 1a718bfa |  |
| 282 | P1 | src/engines/e12_options.py | Python | 129 | 4994b42d |  |
| 283 | P1 | src/engines/e13_contagion.py | Python | 161 | dd7483a4 |  |
| 284 | P1 | src/engines/e14_sentiment.py | Python | 102 | 9da50a2c |  |
| 285 | P1 | src/engines/e15_rl.py | Python | 162 | e333800a |  |
| 286 | P1 | src/engines/e16_adversarial.py | Python | 107 | 0750cb5d |  |
| 287 | P1 | src/engines/e17_liquidity.py | Python | 196 | 24bda7ed |  |
| 288 | P1 | src/engines/e18_network.py | Python | 229 | 58dd9787 |  |
| 289 | P1 | src/engines/orchestrator.py | Python | 491 | 64dd6147 |  |
| 290 | P1 | src/engines/risk_quantifier.py | Python | 63 | aa5769e9 |  |
| 291 | P1 | src/engines/schema.py | Python | 54 | 267f2836 |  |
| 292 | P1 | src/engines/signal_gate.py | Python | 83 | 446f9b8d |  |
| 293 | P1 | src/eventbus/__init__.py | Python | 32 | f081c744 |  |
| 294 | P1 | src/eventbus/bus.py | Python | 374 | 8d7a0597 |  |
| 295 | P1 | src/eventbus/envelope.py | Python | 123 | a6618b0d |  |
| 296 | P1 | src/execution/__init__.py | Python | 1 | 01ba4719 |  |
| 297 | P1 | src/execution/base.py | Python | 134 | d3cad1e1 |  |
| 298 | P1 | src/execution/exchange_contract.py | Python | 310 | 7098433d |  |
| 299 | P1 | src/execution/idempotency.py | Python | 308 | 8eacf415 |  |
| 300 | P1 | src/execution/live_fsm_integration.py | Python | 128 | 65178552 |  |
| 301 | P1 | src/execution/mode_persistence.py | Python | 110 | d236a952 |  |
| 302 | P1 | src/execution/order_manager.py | Python | 585 | 59c1bdb9 |  |
| 303 | P1 | src/execution/order_throttler.py | Python | 244 | eca0b181 |  |
| 304 | P1 | src/execution/paper.py | Python | 1288 | 41889c33 |  |
| 305 | P1 | src/execution/post_trade.py | Python | 253 | 8c262d01 |  |
| 306 | P1 | src/execution/rl_agent.py | Python | 227 | 35eb445b |  |
| 307 | P1 | src/execution/router.py | Python | 477 | 17e8ed36 |  |
| 308 | P1 | src/features/__init__.py | Python | 1 | 01ba4719 |  |
| 309 | P1 | src/features/_rpc_auth.py | Python | 23 | 0a4a04ae |  |
| 310 | P1 | src/features/derivatives.py | Python | 86 | 78bfc557 |  |
| 311 | P1 | src/features/intelligence_features.py | Python | 112 | 085b269c |  |
| 312 | P1 | src/features/mempool.py | Python | 83 | 235bb406 |  |
| 313 | P1 | src/features/microstructure.py | Python | 173 | d890a99f |  |
| 314 | P1 | src/features/nlp.py | Python | 136 | 3908a3e1 |  |
| 315 | P1 | src/features/onchain.py | Python | 170 | 76c3050e |  |
| 316 | P1 | src/features/selftest.py | Python | 63 | 5ec849fa |  |
| 317 | P1 | src/fusion/__init__.py | Python | 1 | e2189aa2 |  |
| 318 | P1 | src/fusion/cross_attention.py | Python | 73 | c6b4c784 |  |
| 319 | P1 | src/fusion/horizon_decision.py | Python | 153 | 593a1838 |  |
| 320 | P1 | src/fusion/meta_network.py | Python | 171 | 4cbe2231 |  |
| 321 | P1 | src/intel.py | Python | 961 | 8353d624 |  |
| 322 | P1 | src/intelligence/__init__.py | Python | 17 | ef4aa7e7 |  |
| 323 | P1 | src/intelligence/calibration.py | Python | 135 | 001de498 |  |
| 324 | P1 | src/intelligence/causal_inference.py | Python | 455 | 3e488b43 |  |
| 325 | P1 | src/intelligence/ensemble_predictor.py | Python | 1057 | 6763a168 |  |
| 326 | P1 | src/intelligence/intelligence_adapter.py | Python | 168 | fb4603f9 |  |
| 327 | P1 | src/intelligence/lstm_runtime.py | Python | 16 | 39702e4d |  |
| 328 | P1 | src/intelligence/macro_indicators.py | Python | 147 | a2289d90 |  |
| 329 | P1 | src/intelligence/macro_regime.py | Python | 79 | 24c6581b |  |
| 330 | P1 | src/intelligence/metrics.py | Python | 299 | fde9d2d5 |  |
| 331 | P1 | src/intelligence/onchain/__init__.py | Python | 52 | b9e4092b |  |
| 332 | P1 | src/intelligence/onchain/arkham_provider.py | Python | 206 | 393c3ba2 |  |
| 333 | P1 | src/intelligence/onchain/base.py | Python | 335 | 5255c1ea |  |
| 334 | P1 | src/intelligence/onchain/coinglass_provider.py | Python | 274 | 989b4baa |  |
| 335 | P1 | src/intelligence/onchain/cryptoquant_provider.py | Python | 248 | 7daa6169 |  |
| 336 | P1 | src/intelligence/onchain/defillama_provider.py | Python | 150 | 8697cd73 |  |
| 337 | P1 | src/intelligence/onchain/dune_provider.py | Python | 230 | 76018eb5 |  |
| 338 | P1 | src/intelligence/onchain/schema.py | Python | 200 | c85cf910 |  |
| 339 | P1 | src/intelligence/probabilistic.py | Python | 460 | 66765aa1 |  |
| 340 | P1 | src/intelligence/probabilistic_adapter.py | Python | 224 | ef336ee8 |  |
| 341 | P1 | src/intelligence/providers/__init__.py | Python | 10 | 074320c3 |  |
| 342 | P1 | src/intelligence/providers/aggregator.py | Python | 500 | 45d5863f |  |
| 343 | P1 | src/intelligence/providers/base.py | Python | 128 | 58a79ab0 |  |
| 344 | P1 | src/intelligence/providers/binance_provider.py | Python | 537 | d0092c66 |  |
| 345 | P1 | src/intelligence/providers/blockchain_provider.py | Python | 193 | bac40269 |  |
| 346 | P1 | src/intelligence/providers/bybit_provider.py | Python | 400 | 22b4da95 |  |
| 347 | P1 | src/intelligence/providers/coingecko_provider.py | Python | 187 | 38c43fab |  |
| 348 | P1 | src/intelligence/providers/okx_provider.py | Python | 417 | a7cf0423 |  |
| 349 | P1 | src/intelligence/risk_quantification.py | Python | 425 | 143bc06f |  |
| 350 | P1 | src/logging_setup.py | Python | 165 | 3563f4c7 |  |
| 351 | P1 | src/mathcore/__init__.py | Python | 38 | dab340e0 |  |
| 352 | P1 | src/mathcore/coding/__init__.py | Python | 18 | a49debd1 |  |
| 353 | P1 | src/mathcore/coding/mds.py | Python | 175 | d438d481 |  |
| 354 | P1 | src/mathcore/coding/reed_solomon.py | Python | 159 | d050f357 |  |
| 355 | P1 | src/mathcore/commitments/__init__.py | Python | 25 | 4340087a |  |
| 356 | P1 | src/mathcore/commitments/merkle.py | Python | 149 | df33035e |  |
| 357 | P1 | src/mathcore/constants/__init__.py | Python | 25 | ac48354d |  |
| 358 | P1 | src/mathcore/constants/nutms.py | Python | 222 | 3036c7bb |  |
| 359 | P1 | src/mathcore/curves/__init__.py | Python | 40 | f8561580 |  |
| 360 | P1 | src/mathcore/curves/bls12_381.py | Python | 396 | 601d10fa |  |
| 361 | P1 | src/mathcore/curves/ed25519.py | Python | 300 | 22d50707 |  |
| 362 | P1 | src/mathcore/curves/secp256k1.py | Python | 355 | bdbb98a3 |  |
| 363 | P1 | src/mathcore/derivation/__init__.py | Python | 73 | 0393fc16 |  |
| 364 | P1 | src/mathcore/derivation/bip32.py | Python | 552 | 77d14b8a |  |
| 365 | P1 | src/mathcore/derivation/nonces.py | Python | 165 | 885f0e28 |  |
| 366 | P1 | src/mathcore/derivation/threshold.py | Python | 419 | d2cce1eb |  |
| 367 | P1 | src/mathcore/fields/__init__.py | Python | 64 | 33acce4e |  |
| 368 | P1 | src/mathcore/fields/binary_field.py | Python | 241 | 894369cc |  |
| 369 | P1 | src/mathcore/fields/interpolation.py | Python | 128 | f50fa25a |  |
| 370 | P1 | src/mathcore/fields/ntt.py | Python | 223 | 929b7cc0 |  |
| 371 | P1 | src/mathcore/fields/prime_field.py | Python | 357 | 8c7553dd |  |
| 372 | P1 | src/mathcore/folklore/__init__.py | Python | 31 | e11fec32 |  |
| 373 | P1 | src/mathcore/folklore/detectors.py | Python | 115 | d592f589 |  |
| 374 | P1 | src/mathcore/folklore/gate.py | Python | 181 | 8aaf7205 |  |
| 375 | P1 | src/mathcore/harmonic/__init__.py | Python | 46 | 2e912222 |  |
| 376 | P1 | src/mathcore/harmonic/fft_spectral.py | Python | 135 | 3ecd676d |  |
| 377 | P1 | src/mathcore/harmonic/gaussian_lattice.py | Python | 194 | 3ae41450 |  |
| 378 | P1 | src/mathcore/harmonic/walsh_hadamard.py | Python | 121 | ae89832f |  |
| 379 | P1 | src/mathcore/lattice/__init__.py | Python | 29 | 673d893c |  |
| 380 | P1 | src/mathcore/lattice/hnp.py | Python | 212 | 484bc27e |  |
| 381 | P1 | src/mathcore/lattice/lll.py | Python | 378 | 301a0c44 |  |
| 382 | P1 | src/mathcore/numbertheory/__init__.py | Python | 96 | b52a8621 |  |
| 383 | P1 | src/mathcore/numbertheory/continued_fractions.py | Python | 104 | bbced475 |  |
| 384 | P1 | src/mathcore/numbertheory/crt.py | Python | 168 | b5cc86b0 |  |
| 385 | P1 | src/mathcore/numbertheory/dlp_bounds.py | Python | 109 | c203bc1e |  |
| 386 | P1 | src/mathcore/numbertheory/factorization.py | Python | 191 | b43fde74 |  |
| 387 | P1 | src/mathcore/numbertheory/primality.py | Python | 315 | 49bc9f93 |  |
| 388 | P1 | src/mathcore/numbertheory/residues.py | Python | 185 | 3d0aef64 |  |
| 389 | P1 | src/mathcore/numbertheory/safe_primes.py | Python | 272 | f1a5ddc4 |  |
| 390 | P1 | src/mathcore/probability/__init__.py | Python | 43 | 3fd3ff8b |  |
| 391 | P1 | src/mathcore/probability/birthday.py | Python | 114 | f1a4ce90 |  |
| 392 | P1 | src/mathcore/probability/committee.py | Python | 147 | 8dad34ad |  |
| 393 | P1 | src/mathcore/probability/confirmations.py | Python | 149 | 66daa523 |  |
| 394 | P1 | src/mathcore/probability/entropy.py | Python | 117 | ef87ac22 |  |
| 395 | P1 | src/mathcore/probability/reorg.py | Python | 105 | b911aed0 |  |
| 396 | P1 | src/mathcore/quantum/__init__.py | Python | 53 | 25b7e2d2 |  |
| 397 | P1 | src/mathcore/quantum/grover.py | Python | 188 | aaa9a864 |  |
| 398 | P1 | src/mathcore/quantum/shor.py | Python | 302 | 934fb820 |  |
| 399 | P1 | src/mathcore/registry.py | Python | 446 | 1130480a |  |
| 400 | P1 | src/models/__init__.py | Python | 1 | 01ba4719 |  |
| 401 | P1 | src/models/architectures.py | Python | 130 | b313c2fa |  |
| 402 | P1 | src/models/bert_head.py | Python | 39 | a1dcbcbc |  |
| 403 | P1 | src/models/cnn.py | Python | 66 | a6d9f953 |  |
| 404 | P1 | src/models/conformer.py | Python | 117 | a3047bc1 |  |
| 405 | P1 | src/models/ecc_head.py | Python | 54 | ac47a72a |  |
| 406 | P1 | src/models/gnn_head.py | Python | 91 | ac22cb11 |  |
| 407 | P1 | src/models/gru.py | Python | 66 | 35715555 |  |
| 408 | P1 | src/models/horizon_backfill.py | Python | 191 | 601be0d0 |  |
| 409 | P1 | src/models/horizon_config.py | Python | 57 | ad98174b |  |
| 410 | P1 | src/models/horizon_learning.py | Python | 1015 | 4b0ac8c1 |  |
| 411 | P1 | src/models/horizon_mlp.py | Python | 338 | b2a1e523 |  |
| 412 | P1 | src/models/leakage.py | Python | 216 | 57616983 |  |
| 413 | P1 | src/models/lstm.py | Python | 51 | 5fcb6568 |  |
| 414 | P1 | src/models/mlp.py | Python | 56 | d79a5eb1 |  |
| 415 | P1 | src/models/nbeats.py | Python | 146 | 0545b607 |  |
| 416 | P1 | src/models/patchtst.py | Python | 97 | 3e54578b |  |
| 417 | P1 | src/models/provenance.py | Python | 364 | 51d1d0d6 |  |
| 418 | P1 | src/models/tcn.py | Python | 125 | a502f868 |  |
| 419 | P1 | src/models/tft.py | Python | 126 | 84df07bb |  |
| 420 | P1 | src/quality/__init__.py | Python | 27 | 56d5dfc7 |  |
| 421 | P1 | src/quality/registry.py | Python | 578 | 297f5bfc |  |
| 422 | P1 | src/regime/__init__.py | Python | 1 | 01ba4719 |  |
| 423 | P1 | src/regime/changepoint.py | Python | 148 | f8b8485e |  |
| 424 | P1 | src/regime/depth_detector_v2.py | Python | 294 | ba9630cc |  |
| 425 | P1 | src/regime/ensemble.py | Python | 84 | f77f8654 |  |
| 426 | P1 | src/regime/garch.py | Python | 220 | 18441bf9 |  |
| 427 | P1 | src/resource_limits.py | Python | 13 | 92f2ac75 |  |
| 428 | P1 | src/risk/__init__.py | Python | 1 | 01ba4719 |  |
| 429 | P1 | src/risk/capital_preservation_floor.py | Python | 206 | 1ef3c083 |  |
| 430 | P1 | src/risk/cognitive_engine.py | Python | 887 | c7cb7324 |  |
| 431 | P1 | src/risk/conflict_resolver.py | Python | 116 | 04e15a2d |  |
| 432 | P1 | src/risk/drift_integration.py | Python | 122 | 71fb03cb |  |
| 433 | P1 | src/risk/execution_cost.py | Python | 154 | 8c6c1c57 |  |
| 434 | P1 | src/risk/gate.py | Python | 155 | 82aabbf1 |  |
| 435 | P1 | src/risk/greeks.py | Python | 108 | f7560515 |  |
| 436 | P1 | src/risk/kelly.py | Python | 862 | c9b80486 |  |
| 437 | P1 | src/risk/macro_exposure_budget.py | Python | 180 | c73111ed |  |
| 438 | P1 | src/risk/paper_qualification.py | Python | 323 | c1de14b0 |  |
| 439 | P1 | src/risk/performance_drift.py | Python | 608 | 8be6b0d3 |  |
| 440 | P1 | src/risk/portfolio_agreement.py | Python | 170 | 4581c82a |  |
| 441 | P1 | src/risk/portfolio_correlation.py | Python | 333 | 2a5c7e12 |  |
| 442 | P1 | src/risk/slippage.py | Python | 227 | f8525b31 |  |
| 443 | P1 | src/risk/state_persistence.py | Python | 71 | 6dddbf97 |  |
| 444 | P1 | src/risk/strategy_correlation.py | Python | 108 | 2d26d59b |  |
| 445 | P1 | src/risk/strategy_decay.py | Python | 71 | 40d00f5d |  |
| 446 | P1 | src/risk/strategy_kill_switch.py | Python | 541 | 6dc9fb70 |  |
| 447 | P1 | src/risk/vol_target_sizer.py | Python | 293 | 5dfc598a |  |
| 448 | P1 | src/runtime/__init__.py | Python | 27 | 8fa60c2b |  |
| 449 | P1 | src/runtime/adapters.py | Python | 730 | 930db9da |  |
| 450 | P1 | src/runtime/adaptive.py | Python | 341 | 49379dd1 |  |
| 451 | P1 | src/runtime/classification.py | Python | 78 | 9bf41945 |  |
| 452 | P1 | src/runtime/controllers.py | Python | 244 | 1f6ecb90 |  |
| 453 | P1 | src/runtime/dependencies.py | Python | 237 | a8e6fe3d |  |
| 454 | P1 | src/runtime/events.py | Python | 82 | d1b1ee54 |  |
| 455 | P1 | src/runtime/horizon_models.py | Python | 258 | 40b63730 |  |
| 456 | P1 | src/runtime/persistence.py | Python | 223 | 3d2debe2 |  |
| 457 | P1 | src/runtime/reconcile.py | Python | 303 | e3ebc015 |  |
| 458 | P1 | src/runtime/registry.py | Python | 537 | c2307736 |  |
| 459 | P1 | src/runtime/supervisor.py | Python | 454 | 37a709f2 |  |
| 460 | P1 | src/security/__init__.py | Python | 10 | 04ce86e6 |  |
| 461 | P1 | src/security/api_signer.py | Python | 279 | 08b626dd |  |
| 462 | P1 | src/security/at_rest.py | Python | 152 | 95820b10 |  |
| 463 | P1 | src/security/constant_time.py | Python | 137 | 5577b1ef |  |
| 464 | P1 | src/security/credential_vault.py | Python | 136 | c3cf6658 |  |
| 465 | P1 | src/security/exchange_key_posture.py | Python | 186 | 38082cf0 |  |
| 466 | P1 | src/security/key_lifecycle.py | Python | 180 | 62b00db2 |  |
| 467 | P1 | src/security/pq_transport.py | Python | 131 | f4eb4fea |  |
| 468 | P1 | src/security/randomness.py | Python | 115 | d626d758 |  |
| 469 | P1 | src/security/ssrf.py | Python | 191 | 4e5bd58c |  |
| 470 | P1 | src/security/tls.py | Python | 121 | 4eef92c8 |  |
| 471 | P1 | src/strategies/__init__.py | Python | 0 | e3b0c442 |  |
| 472 | P1 | src/strategies/basis_trade.py | Python | 116 | adffe19c |  |
| 473 | P1 | src/strategies/breakout.py | Python | 106 | dddeb580 |  |
| 474 | P1 | src/strategies/capital_allocator.py | Python | 289 | 6420c963 |  |
| 475 | P1 | src/strategies/cross_exchange_arb.py | Python | 88 | 87eaa25e |  |
| 476 | P1 | src/strategies/filters.py | Python | 621 | 18fc5c6b |  |
| 477 | P1 | src/strategies/funding_carry.py | Python | 103 | ffb40e4c |  |
| 478 | P1 | src/strategies/mean_reversion.py | Python | 130 | 13464d4f |  |
| 479 | P1 | src/strategies/options_carry.py | Python | 170 | ccb47143 |  |
| 480 | P1 | src/strategies/position_sizing.py | Python | 437 | 2de26394 |  |
| 481 | P1 | src/strategies/regime_strategy_selector.py | Python | 273 | 13bdbe81 |  |
| 482 | P1 | src/strategies/signal_engine_adapter.py | Python | 63 | 762dcb31 |  |
| 483 | P1 | src/strategies/xsec_momentum.py | Python | 91 | a1adb1b6 |  |
| 484 | P1 | src/terminal/__init__.py | Python | 22 | f18c9e3b |  |
| 485 | P1 | src/terminal/__main__.py | Python | 10 | 155cb5e6 |  |
| 486 | P1 | src/terminal/auth.py | Python | 98 | 01b5dabc |  |
| 487 | P1 | src/terminal/buffer.py | Python | 62 | ff135249 |  |
| 488 | P1 | src/terminal/cli.py | Python | 806 | 441badbd |  |
| 489 | P1 | src/terminal/client.py | Python | 132 | 9dd1534e |  |
| 490 | P1 | src/terminal/config.py | Python | 339 | 1a2b741a |  |
| 491 | P1 | src/terminal/install.py | Python | 247 | 45fb9ae9 |  |
| 492 | P1 | src/terminal/jobs.py | Python | 150 | 7e534013 |  |
| 493 | P1 | src/terminal/markers.py | Python | 118 | 22ca7f09 |  |
| 494 | P1 | src/terminal/procfs.py | Python | 138 | 8d50fef6 |  |
| 495 | P1 | src/terminal/registry.py | Python | 268 | c26222ec |  |
| 496 | P1 | src/terminal/sessions.py | Python | 739 | d38e7d87 |  |
| 497 | P1 | src/terminal/shell_integration.py | Python | 72 | b13343f7 |  |
| 498 | P1 | src/tuning/__init__.py | Python | 9 | bef3b3ff |  |
| 499 | P1 | src/tuning/audit.py | Python | 142 | 2be43241 |  |
| 500 | P1 | src/tuning/backtest_harness.py | Python | 697 | 3aff84bf |  |
| 501 | P1 | src/tuning/bayesian_proposer.py | Python | 106 | a627571c |  |
| 502 | P1 | src/tuning/bootstrap.py | Python | 368 | a02f4e2a |  |
| 503 | P1 | src/tuning/engine_backtest.py | Python | 352 | 72758591 |  |
| 504 | P1 | src/tuning/evaluator.py | Python | 276 | 390f6db5 |  |
| 505 | P1 | src/tuning/factor_search.py | Python | 164 | 87889afc |  |
| 506 | P1 | src/tuning/gate.py | Python | 113 | eed4dd5c |  |
| 507 | P1 | src/tuning/live_overrides.py | Python | 178 | 7dfe7bea |  |
| 508 | P1 | src/tuning/meta_allocator.py | Python | 173 | 959d64f2 |  |
| 509 | P1 | src/tuning/promotion_gauntlet.py | Python | 140 | c5ddaf51 |  |
| 510 | P1 | src/tuning/proposer.py | Python | 74 | ac1d5607 |  |
| 511 | P1 | src/tuning/redteam_scheduler.py | Python | 63 | 0fbe8723 |  |
| 512 | P1 | src/tuning/registry.py | Python | 170 | fc917aa4 |  |
| 513 | P1 | src/tuning/runner.py | Python | 352 | 43d993ab |  |
| 514 | P1 | src/tuning/state.py | Python | 113 | 3bbf0ea6 |  |
| 515 | P1 | src/tuning/store.py | Python | 208 | b74a8cb4 |  |
| 516 | P1 | src/tuning/stress_simulator.py | Python | 109 | 18d69055 |  |
| 517 | P1 | src/tuning/watchdog.py | Python | 205 | fc8dd98a |  |
| 518 | P1 | src/upgrade/__init__.py | Python | 0 | e3b0c442 |  |
| 519 | P1 | src/upgrade/maml.py | Python | 181 | 270e0de0 |  |
| 520 | P1 | src/upgrade/optuna_wf.py | Python | 229 | 326f0f0b |  |
| 521 | P1 | src/upgrade/registry.py | Python | 246 | 7d7848e1 |  |
| 522 | P1 | src/upgrade/shadow_deploy.py | Python | 304 | 96f01c41 |  |
| 523 | P1 | src/workers/__init__.py | Python | 1 | ee15cb65 |  |
| 524 | P1 | src/workers/__main__.py | Python | 12 | b2b41fb1 |  |
| 525 | P1 | tests/agent_control/__init__.py | Python | 0 | e3b0c442 |  |
| 526 | P1 | tests/agent_control/conftest.py | Python | 123 | 8bce4f3e |  |
| 527 | P1 | tests/agent_control/test_branch_audit.py | Python | 277 | c2e5d55e |  |
| 528 | P1 | tests/agent_control/test_cli.py | Python | 310 | 63625b96 |  |
| 529 | P1 | tests/agent_control/test_completion.py | Python | 323 | 85e4eca9 |  |
| 530 | P1 | tests/agent_control/test_git_safety.py | Python | 238 | 52c26003 |  |
| 531 | P1 | tests/agent_control/test_gitstate.py | Python | 279 | 5910e557 |  |
| 532 | P1 | tests/agent_control/test_hooks.py | Python | 224 | 2de9ab66 |  |
| 533 | P1 | tests/agent_control/test_model.py | Python | 471 | b7fdd280 |  |
| 534 | P1 | tests/agent_control/test_reliability.py | Python | 324 | fcd2b87a |  |
| 535 | P1 | tests/agent_control/test_store.py | Python | 148 | 3d540971 |  |
| 536 | P1 | tests/agent_control/test_workspace.py | Python | 354 | 57897d20 |  |
| 537 | P1 | tests/api/__init__.py | Python | 0 | e3b0c442 |  |
| 538 | P1 | tests/api/test_authz_and_secrets.py | Python | 310 | a24c69e4 |  |
| 539 | P1 | tests/api/test_error_hygiene.py | Python | 288 | 749686a5 |  |
| 540 | P1 | tests/api/test_fail_closed_controls.py | Python | 181 | f3a5af5f |  |
| 541 | P1 | tests/api/test_injection_and_rate_limiting.py | Python | 283 | 7dc17358 |  |
| 542 | P1 | tests/api/test_kill_switch_durability.py | Python | 164 | d3358cb3 |  |
| 543 | P1 | tests/api/test_security_headers.py | Python | 225 | f136203f |  |
| 544 | P1 | tests/api/test_ssrf_protection.py | Python | 270 | 0309ccc9 |  |
| 545 | P1 | tests/api/test_websocket_frame_guard.py | Python | 258 | a13bf930 |  |
| 546 | P1 | tests/authentication/__init__.py | Python | 0 | e3b0c442 |  |
| 547 | P1 | tests/authentication/test_api_authentication.py | Python | 207 | 7fd81d32 |  |
| 548 | P1 | tests/authorization/__init__.py | Python | 0 | e3b0c442 |  |
| 549 | P1 | tests/authorization/test_authorization_matrix.py | Python | 194 | 23135614 |  |
| 550 | P1 | tests/authorization/test_object_references.py | Python | 183 | fe2a77b6 |  |
| 551 | P1 | tests/component/__init__.py | Python | 0 | e3b0c442 |  |
| 552 | P1 | tests/component/test_clock_policy.py | Python | 164 | 2b63ae2d |  |
| 553 | P1 | tests/component/test_data_quality_gate.py | Python | 474 | cce1da8a |  |
| 554 | P1 | tests/component/test_money_representation.py | Python | 231 | 44d8855e |  |
| 555 | P1 | tests/conftest.py | Python | 358 | 65b337e1 |  |
| 556 | P1 | tests/contract/__init__.py | Python | 0 | e3b0c442 |  |
| 557 | P1 | tests/contract/test_exchange_order_contract.py | Python | 242 | 75a6c856 |  |
| 558 | P1 | tests/engines/__init__.py | Python | 0 | e3b0c442 |  |
| 559 | P1 | tests/engines/test_adapter_wiring.py | Python | 70 | 4916ed8a |  |
| 560 | P1 | tests/engines/test_backtest.py | Python | 126 | 3107dc69 |  |
| 561 | P1 | tests/engines/test_backtest_runners.py | Python | 231 | 58c8a2f7 |  |
| 562 | P1 | tests/engines/test_consensus.py | Python | 264 | 96a251ef |  |
| 563 | P1 | tests/engines/test_consensus_edges.py | Python | 158 | 8b8e3146 |  |
| 564 | P1 | tests/engines/test_crypto_box_adapter.py | Python | 89 | 27cb79da |  |
| 565 | P1 | tests/engines/test_data_providers.py | Python | 140 | f6ed3e19 |  |
| 566 | P1 | tests/engines/test_data_providers_extended.py | Python | 208 | 0d544565 |  |
| 567 | P1 | tests/engines/test_depth_detector_v2.py | Python | 162 | 58259645 |  |
| 568 | P1 | tests/engines/test_deribit_provider.py | Python | 158 | 39492821 |  |
| 569 | P1 | tests/engines/test_e17_orderbook_and_scale.py | Python | 116 | deedd476 |  |
| 570 | P1 | tests/engines/test_engine_guard_and_error_paths.py | Python | 624 | f0ecef2f |  |
| 571 | P1 | tests/engines/test_engine_paths.py | Python | 847 | 9db4e39c |  |
| 572 | P1 | tests/engines/test_engines_unit.py | Python | 881 | a6e2bb3b |  |
| 573 | P1 | tests/engines/test_flow_and_height_providers.py | Python | 198 | 4f67b2aa |  |
| 574 | P1 | tests/engines/test_manipulation_and_liquidity.py | Python | 236 | 983733cc |  |
| 575 | P1 | tests/engines/test_orchestrator.py | Python | 151 | 29a619eb |  |
| 576 | P1 | tests/engines/test_provider_cache.py | Python | 73 | 8885885f |  |
| 577 | P1 | tests/engines/test_risk_quantifier.py | Python | 55 | 4fa24690 |  |
| 578 | P1 | tests/engines/test_schema.py | Python | 44 | e8c4e0f2 |  |
| 579 | P1 | tests/engines/test_security.py | Python | 147 | 50513634 |  |
| 580 | P1 | tests/engines/test_sentiment_provider.py | Python | 228 | 00742d4a |  |
| 581 | P1 | tests/engines/test_signal_gate.py | Python | 72 | 09d639bd |  |
| 582 | P1 | tests/engines/test_supply_and_quality.py | Python | 127 | 6a9dd379 |  |
| 583 | P1 | tests/execution/__init__.py | Python | 0 | e3b0c442 |  |
| 584 | P1 | tests/execution/test_idempotency_end_to_end.py | Python | 251 | 80e6ae28 |  |
| 585 | P1 | tests/execution/test_order_fsm_totality.py | Python | 255 | e76f01d1 |  |
| 586 | P1 | tests/execution/test_venue_precision.py | Python | 195 | ae997cde |  |
| 587 | P1 | tests/features/__init__.py | Python | 0 | e3b0c442 |  |
| 588 | P1 | tests/features/test_closed_bar_inference.py | Python | 47 | 03bdc756 |  |
| 589 | P1 | tests/features/test_feature_determinism.py | Python | 220 | 3fb9be0c |  |
| 590 | P1 | tests/fixtures/signals/BTCUSDT_15m_case_001.json | JSON | 63 | 5da10c05 |  |
| 591 | P1 | tests/fixtures/signals/BTCUSDT_15m_case_002.json | JSON | 63 | 413041da |  |
| 592 | P1 | tests/fixtures/signals/BTCUSDT_15m_case_003.json | JSON | 63 | 270784b7 |  |
| 593 | P1 | tests/fixtures/signals/ETHUSDT_15m_case_001.json | JSON | 64 | 1bc7bdcf |  |
| 594 | P1 | tests/fixtures/signals/ETHUSDT_15m_case_002.json | JSON | 43 | 044b27e5 |  |
| 595 | P1 | tests/fixtures/signals/ETHUSDT_15m_case_003.json | JSON | 45 | 75426f64 |  |
| 596 | P1 | tests/fuzz/__init__.py | Python | 0 | e3b0c442 |  |
| 597 | P1 | tests/fuzz/test_malformed_input_is_safe.py | Python | 291 | 14090dac |  |
| 598 | P1 | tests/intelligence/__init__.py | Python | 0 | e3b0c442 |  |
| 599 | P1 | tests/intelligence/onchain/__init__.py | Python | 0 | e3b0c442 |  |
| 600 | P1 | tests/intelligence/onchain/test_arkham_provider.py | Python | 261 | 3dd22d48 |  |
| 601 | P1 | tests/intelligence/onchain/test_base.py | Python | 147 | e7044b9f |  |
| 602 | P1 | tests/intelligence/onchain/test_coinglass_provider.py | Python | 333 | d64ae3a5 |  |
| 603 | P1 | tests/intelligence/onchain/test_cryptoquant_provider.py | Python | 316 | b41b126d |  |
| 604 | P1 | tests/intelligence/onchain/test_defillama_provider.py | Python | 204 | f2874f66 |  |
| 605 | P1 | tests/intelligence/onchain/test_dune_provider.py | Python | 341 | dffadbc8 |  |
| 606 | P1 | tests/intelligence/onchain/test_onchain_aggregator_integration.py | Python | 207 | 646628db |  |
| 607 | P1 | tests/intelligence/onchain/test_onchain_gating.py | Python | 118 | b94ff04b |  |
| 608 | P1 | tests/intelligence/onchain/test_schema.py | Python | 203 | 2b7240df |  |
| 609 | P1 | tests/models/__init__.py | Python | 0 | e3b0c442 |  |
| 610 | P1 | tests/models/test_cpcv_purging.py | Python | 180 | 16aaebcd |  |
| 611 | P1 | tests/models/test_lookahead.py | Python | 273 | bfd4bced |  |
| 612 | P1 | tests/models/test_model_artifacts.py | Python | 237 | da56233f |  |
| 613 | P1 | tests/models/test_model_drift_demotion.py | Python | 245 | 023b0416 |  |
| 614 | P1 | tests/models/test_model_provenance.py | Python | 413 | 40defb51 |  |
| 615 | P1 | tests/models/test_model_safety.py | Python | 180 | 2f832c68 |  |
| 616 | P1 | tests/models/test_research_firewall.py | Python | 258 | 92dac5eb |  |
| 617 | P1 | tests/performance/__init__.py | Python | 0 | e3b0c442 |  |
| 618 | P1 | tests/performance/test_performance_baselines.py | Python | 217 | bcb11a27 |  |
| 619 | P1 | tests/portfolio/__init__.py | Python | 0 | e3b0c442 |  |
| 620 | P1 | tests/portfolio/test_portfolio_limits.py | Python | 252 | f6326b7b |  |
| 621 | P1 | tests/production/__init__.py | Python | 0 | e3b0c442 |  |
| 622 | P1 | tests/production/test_behavioural_guard.py | Python | 155 | 2451908c |  |
| 623 | P1 | tests/production/test_halt_triggers.py | Python | 176 | 49c26802 |  |
| 624 | P1 | tests/production/test_production_gate.py | Python | 212 | 52a13c99 |  |
| 625 | P1 | tests/production/test_startup_selftest.py | Python | 188 | 665c9c6b |  |
| 626 | P1 | tests/property/__init__.py | Python | 0 | e3b0c442 |  |
| 627 | P1 | tests/property/test_position_sizing_properties.py | Python | 245 | 50ec596c |  |
| 628 | P1 | tests/pyg_stub.py | Python | 74 | 9ec25dff |  |
| 629 | P1 | tests/qualification/__init__.py | Python | 0 | e3b0c442 |  |
| 630 | P1 | tests/qualification/test_paper_qualification.py | Python | 348 | 4b77680d |  |
| 631 | P1 | tests/qualification/test_self_tuning_firewall.py | Python | 186 | c81f7179 |  |
| 632 | P1 | tests/quality/__init__.py | Python | 0 | e3b0c442 |  |
| 633 | P1 | tests/quality/test_qe_id_allocation.py | Python | 226 | 926782b5 |  |
| 634 | P1 | tests/quality/test_qe_skill.py | Python | 358 | 1a667c83 |  |
| 635 | P1 | tests/quality/test_quality_docs_in_sync.py | Python | 72 | ef1e542a |  |
| 636 | P1 | tests/quality/test_quality_registry.py | Python | 802 | fb2963cb |  |
| 637 | P1 | tests/quality/test_quality_registry_schema.py | Python | 268 | 4b19c115 |  |
| 638 | P1 | tests/recovery/__init__.py | Python | 0 | e3b0c442 |  |
| 639 | P1 | tests/recovery/test_chaos_suite.py | Python | 173 | ead89296 |  |
| 640 | P1 | tests/recovery/test_concurrency_races.py | Python | 202 | 431870be |  |
| 641 | P1 | tests/recovery/test_crash_replay.py | Python | 245 | ca6bb263 |  |
| 642 | P1 | tests/recovery/test_failsafe_policy.py | Python | 167 | 1af08f6a |  |
| 643 | P1 | tests/recovery/test_recovery_objectives.py | Python | 198 | 00a98f52 |  |
| 644 | P1 | tests/regime/__init__.py | Python | 0 | e3b0c442 |  |
| 645 | P1 | tests/regime/test_garch.py | Python | 148 | 8a4195c0 |  |
| 646 | P1 | tests/regression/__init__.py | Python | 0 | e3b0c442 |  |
| 647 | P1 | tests/regression/test_ci_failure_locks.py | Python | 67 | 6c0933bb |  |
| 648 | P1 | tests/regression/test_halts_drift_failclosed.py | Python | 193 | caf02ccc |  |
| 649 | P1 | tests/regression/test_metrics_payload.py | Python | 120 | 094976c7 |  |
| 650 | P1 | tests/regression/test_phase6_math_strategy_lows.py | Python | 163 | b2ced63e |  |
| 651 | P1 | tests/regression/test_regression_registry_contract.py | Python | 852 | 2c503005 |  |
| 652 | P1 | tests/regression/unraisable.py | Python | 19 | 8f8b1064 |  |
| 653 | P1 | tests/required_import.py | Python | 22 | 14788dee |  |
| 654 | P1 | tests/risk/__init__.py | Python | 0 | e3b0c442 |  |
| 655 | P1 | tests/risk/test_probability_bounds.py | Python | 137 | a3b65a78 |  |
| 656 | P1 | tests/risk/test_risk_limit_boundaries.py | Python | 300 | 37b9b36e |  |
| 657 | P1 | tests/runtime/__init__.py | Python | 0 | e3b0c442 |  |
| 658 | P1 | tests/runtime/_production.py | Python | 128 | bb4e5d02 |  |
| 659 | P1 | tests/runtime/_support.py | Python | 126 | df465141 |  |
| 660 | P1 | tests/runtime/conftest.py | Python | 12 | 8b454b0c |  |
| 661 | P1 | tests/runtime/test_adaptive_lifecycle.py | Python | 196 | b074db7e |  |
| 662 | P1 | tests/runtime/test_bounded_control_plane.py | Python | 121 | 06cd3bec |  |
| 663 | P1 | tests/runtime/test_capabilities.py | Python | 81 | b97da1aa |  |
| 664 | P1 | tests/runtime/test_causal_tracing.py | Python | 191 | f4f60285 |  |
| 665 | P1 | tests/runtime/test_change_authorization.py | Python | 74 | 37958ed3 |  |
| 666 | P1 | tests/runtime/test_change_manager.py | Python | 172 | 53304d88 |  |
| 667 | P1 | tests/runtime/test_concurrency.py | Python | 70 | 3b3fc64f |  |
| 668 | P1 | tests/runtime/test_continuous_reconciliation.py | Python | 246 | db640638 |  |
| 669 | P1 | tests/runtime/test_contracts.py | Python | 205 | bcdfaada |  |
| 670 | P1 | tests/runtime/test_controller_contracts.py | Python | 208 | a16e4161 |  |
| 671 | P1 | tests/runtime/test_dependencies.py | Python | 73 | 3e5fe2b2 |  |
| 672 | P1 | tests/runtime/test_dependency_cycles.py | Python | 59 | 9c9ed6f7 |  |
| 673 | P1 | tests/runtime/test_desired_state.py | Python | 156 | 1a6f8e00 |  |
| 674 | P1 | tests/runtime/test_engine_tracing.py | Python | 165 | 6f6e13d9 |  |
| 675 | P1 | tests/runtime/test_failure_injection.py | Python | 204 | 149ddccb |  |
| 676 | P1 | tests/runtime/test_impact_analysis.py | Python | 91 | ba6dd5c1 |  |
| 677 | P1 | tests/runtime/test_integration.py | Python | 116 | 1af73002 |  |
| 678 | P1 | tests/runtime/test_lifecycle.py | Python | 98 | 53c2bc30 |  |
| 679 | P1 | tests/runtime/test_production_controllers.py | Python | 210 | 8af825c2 |  |
| 680 | P1 | tests/runtime/test_production_runtime.py | Python | 312 | 67f5b0db |  |
| 681 | P1 | tests/runtime/test_promotion_gates.py | Python | 30 | 11cc41e1 |  |
| 682 | P1 | tests/runtime/test_reconciliation.py | Python | 133 | 0da8ef79 |  |
| 683 | P1 | tests/runtime/test_recovery.py | Python | 104 | 05e3dcba |  |
| 684 | P1 | tests/runtime/test_registry.py | Python | 216 | 9d20d15a |  |
| 685 | P1 | tests/runtime/test_registry_adapters.py | Python | 228 | b36d5369 |  |
| 686 | P1 | tests/runtime/test_registry_identity.py | Python | 87 | 84d0a300 |  |
| 687 | P1 | tests/runtime/test_registry_resync.py | Python | 217 | 1e61af91 |  |
| 688 | P1 | tests/runtime/test_rollback.py | Python | 84 | 1d543635 |  |
| 689 | P1 | tests/runtime/test_rollout.py | Python | 128 | b69600b3 |  |
| 690 | P1 | tests/runtime/test_runtime_endpoints.py | Python | 272 | e598bffe |  |
| 691 | P1 | tests/runtime/test_runtime_loop_resilience.py | Python | 184 | 878f7724 |  |
| 692 | P1 | tests/runtime/test_runtime_safety.py | Python | 340 | 7b3cb9d3 |  |
| 693 | P1 | tests/runtime/test_runtime_state.py | Python | 47 | 2bd44e1f |  |
| 694 | P1 | tests/runtime/test_supervisor_failures.py | Python | 124 | e3c6ab66 |  |
| 695 | P1 | tests/runtime/test_supervisors.py | Python | 220 | fc8b9145 |  |
| 696 | P1 | tests/security/__init__.py | Python | 0 | e3b0c442 |  |
| 697 | P1 | tests/security/test_at_rest_encryption.py | Python | 180 | bffe6f38 |  |
| 698 | P1 | tests/security/test_audit_chain_tamper_evidence.py | Python | 213 | c38f3d7d |  |
| 699 | P1 | tests/security/test_exchange_key_posture.py | Python | 199 | 903dc8cc |  |
| 700 | P1 | tests/security/test_filelock_cve_floor.py | Python | 48 | 6349f915 |  |
| 701 | P1 | tests/security/test_gitignore_secret_files.py | Python | 109 | 0b6a69d2 |  |
| 702 | P1 | tests/security/test_key_lifecycle.py | Python | 164 | c9167446 |  |
| 703 | P1 | tests/security/test_no_custom_primitives.py | Python | 231 | f46e5ca8 |  |
| 704 | P1 | tests/security/test_npm_audit_fix_available_gate.py | Python | 368 | 85de0d16 |  |
| 705 | P1 | tests/security/test_randomness_and_tls.py | Python | 238 | 43a0cb62 |  |
| 706 | P1 | tests/security/test_secret_leak_provocation.py | Python | 134 | d1d4041f |  |
| 707 | P1 | tests/security/test_signing_and_constant_time.py | Python | 230 | 0cf7fdfc |  |
| 708 | P1 | tests/security/test_urllib3_cve_floor.py | Python | 47 | 48687978 |  |
| 709 | P1 | tests/signals/__init__.py | Python | 0 | e3b0c442 |  |
| 710 | P1 | tests/signals/golden.py | Python | 321 | 7d6fc493 |  |
| 711 | P1 | tests/signals/test_golden_signals.py | Python | 166 | a7893a63 |  |
| 712 | P1 | tests/supply_chain/__init__.py | Python | 0 | e3b0c442 |  |
| 713 | P1 | tests/supply_chain/test_artifact_provenance.py | Python | 162 | 9c1cf238 |  |
| 714 | P1 | tests/supply_chain/test_container_posture.py | Python | 177 | c88c57a9 |  |
| 715 | P1 | tests/supply_chain/test_supply_chain_posture.py | Python | 466 | 8025b432 |  |
| 716 | P1 | tests/terminal/__init__.py | Python | 0 | e3b0c442 |  |
| 717 | P1 | tests/terminal/_support.py | Python | 350 | 06109a83 |  |
| 718 | P1 | tests/terminal/conftest.py | Python | 50 | b7931e73 |  |
| 719 | P1 | tests/terminal/test_terminal_cli.py | Python | 651 | 18fae5bf |  |
| 720 | P1 | tests/terminal/test_terminal_host.py | Python | 284 | 342b5d4a |  |
| 721 | P1 | tests/terminal/test_terminal_install_jobs.py | Python | 301 | 2cc29f89 |  |
| 722 | P1 | tests/terminal/test_terminal_markers_buffer.py | Python | 104 | 9e5c40b8 |  |
| 723 | P1 | tests/terminal/test_terminal_protocol.py | Python | 161 | 57c8c650 |  |
| 724 | P1 | tests/terminal/test_terminal_registry.py | Python | 167 | 54ed8244 |  |
| 725 | P1 | tests/terminal/test_terminal_server.py | Python | 540 | e767a615 |  |
| 726 | P1 | tests/terminal/test_terminal_sessions.py | Python | 439 | 08e7a756 |  |
| 727 | P1 | tests/test_access_control.py | Python | 57 | 504259f9 |  |
| 728 | P1 | tests/test_access_control_wiring.py | Python | 143 | 64d001ec |  |
| 729 | P1 | tests/test_agent_reliability_boundary.py | Python | 39 | e9e2d4ba |  |
| 730 | P1 | tests/test_api_and_fsm_coverage.py | Python | 176 | b0cfe603 |  |
| 731 | P1 | tests/test_api_auth_middleware.py | Python | 234 | 33be5fe7 |  |
| 732 | P1 | tests/test_api_dunder_main.py | Python | 49 | b2a7da69 |  |
| 733 | P1 | tests/test_api_main_coverage.py | Python | 1692 | 913e445f |  |
| 734 | P1 | tests/test_api_main_edges.py | Python | 107 | 5b383da8 |  |
| 735 | P1 | tests/test_api_main_endpoints_coverage.py | Python | 505 | b4a50b87 |  |
| 736 | P1 | tests/test_api_operations_endpoints.py | Python | 203 | fae70eb8 |  |
| 737 | P1 | tests/test_api_role_enforcement.py | Python | 174 | 4e7cff8d |  |
| 738 | P1 | tests/test_api_signer_audit.py | Python | 174 | fff8d678 |  |
| 739 | P1 | tests/test_api_terminal_jobs.py | Python | 196 | ba84a1ac |  |
| 740 | P1 | tests/test_apply_ci_patch.py | Python | 109 | 43624da5 |  |
| 741 | P1 | tests/test_apply_repo_ruleset.py | Python | 288 | e1799986 |  |
| 742 | P1 | tests/test_arch_baseline_is_current.py | Python | 79 | 1ae91139 |  |
| 743 | P1 | tests/test_architecture_layers.py | Python | 181 | 954aa9c3 |  |
| 744 | P1 | tests/test_assert_jobs_green.py | Python | 244 | d7a5bcca |  |
| 745 | P1 | tests/test_attribution.py | Python | 267 | 79185ed1 |  |
| 746 | P1 | tests/test_audit_chain_integrity_endpoint.py | Python | 167 | eeb84b92 |  |
| 747 | P1 | tests/test_audit_trail.py | Python | 81 | ce39ac7b |  |
| 748 | P1 | tests/test_audit_trail_bounded.py | Python | 87 | 7f027a79 |  |
| 749 | P1 | tests/test_basis_trade.py | Python | 141 | 91778723 |  |
| 750 | P1 | tests/test_binary_field.py | Python | 279 | f9f3d0af |  |
| 751 | P1 | tests/test_bip32.py | Python | 673 | c15f0915 |  |
| 752 | P1 | tests/test_birthday.py | Python | 134 | 90ef283f |  |
| 753 | P1 | tests/test_bls12_381.py | Python | 170 | 29a4e941 |  |
| 754 | P1 | tests/test_breakout.py | Python | 98 | 3c5fc7a8 |  |
| 755 | P1 | tests/test_calibration.py | Python | 114 | 2514e0b9 |  |
| 756 | P1 | tests/test_capital_allocator.py | Python | 303 | a5e4e9e9 |  |
| 757 | P1 | tests/test_capital_allocator_edges.py | Python | 154 | 5e5831b6 |  |
| 758 | P1 | tests/test_capital_preservation_floor.py | Python | 128 | daacb978 |  |
| 759 | P1 | tests/test_causal_asset_gnn.py | Python | 114 | e3a52934 |  |
| 760 | P1 | tests/test_causal_asset_gnn_pyg.py | Python | 78 | b3e0219f |  |
| 761 | P1 | tests/test_causal_dowhy_scm.py | Python | 125 | 7eb0139c |  |
| 762 | P1 | tests/test_causal_inference.py | Python | 243 | 917865bc |  |
| 763 | P1 | tests/test_causal_modules.py | Python | 220 | ae5d9554 |  |
| 764 | P1 | tests/test_changepoint.py | Python | 123 | e4fefb9a |  |
| 765 | P1 | tests/test_ci_diagnostics.py | Python | 462 | ac1855cc |  |
| 766 | P1 | tests/test_ci_diagnostics_log_unavailable.py | Python | 117 | a5b82fb8 |  |
| 767 | P1 | tests/test_ci_diagnostics_never_self_blocks.py | Python | 169 | 006fd261 |  |
| 768 | P1 | tests/test_ci_failure_notify_workflow.py | Python | 54 | de207c83 |  |
| 769 | P1 | tests/test_ci_log_access.py | Python | 320 | 71f874d0 |  |
| 770 | P1 | tests/test_ci_notice_supersession.py | Python | 65 | e65d0b45 |  |
| 771 | P1 | tests/test_ci_workflow_cost.py | Python | 235 | fb0a0315 |  |
| 772 | P1 | tests/test_codebase_knowledge_index.py | Python | 216 | d45bbe00 |  |
| 773 | P1 | tests/test_codex_pr_handoff.py | Python | 296 | 38f498d9 |  |
| 774 | P1 | tests/test_coding.py | Python | 176 | c980e95b |  |
| 775 | P1 | tests/test_cognitive_engine.py | Python | 700 | 0e658cfe |  |
| 776 | P1 | tests/test_command_schema_policy.py | Python | 382 | 09d4ee2e |  |
| 777 | P1 | tests/test_common_claude_cli.py | Python | 129 | 4eaba7c6 |  |
| 778 | P1 | tests/test_config.py | Python | 164 | 7cbfdba0 |  |
| 779 | P1 | tests/test_config_feature_settings.py | Python | 28 | 980e84d3 |  |
| 780 | P1 | tests/test_config_strategy_field.py | Python | 54 | bf6fe6b9 |  |
| 781 | P1 | tests/test_confirmations.py | Python | 195 | c2e28bc8 |  |
| 782 | P1 | tests/test_constant_time_timing.py | Python | 114 | 3d301fe7 |  |
| 783 | P1 | tests/test_control_surface.py | Python | 330 | d262e989 |  |
| 784 | P1 | tests/test_control_write.py | Python | 239 | 605c0718 |  |
| 785 | P1 | tests/test_coverage_boost.py | Python | 446 | a3a83684 |  |
| 786 | P1 | tests/test_coverage_boost2.py | Python | 394 | e911097a |  |
| 787 | P1 | tests/test_coverage_boost3.py | Python | 738 | 813901ba |  |
| 788 | P1 | tests/test_coverage_boost4.py | Python | 311 | 4776b184 |  |
| 789 | P1 | tests/test_coverage_boost5.py | Python | 572 | 7908050d |  |
| 790 | P1 | tests/test_coverage_boost6.py | Python | 196 | 3ab4d6b6 |  |
| 791 | P1 | tests/test_coverage_mid_batch.py | Python | 254 | 94b0772c |  |
| 792 | P1 | tests/test_cross_exchange_arb.py | Python | 105 | 74948a3a |  |
| 793 | P1 | tests/test_crt.py | Python | 236 | dd77ffd3 |  |
| 794 | P1 | tests/test_crypto_architect_skill.py | Python | 359 | 5730d555 |  |
| 795 | P1 | tests/test_crypto_intel_main.py | Python | 166 | c76abb0b |  |
| 796 | P1 | tests/test_crypto_intel_signal_path.py | Python | 733 | 68ff99b3 |  |
| 797 | P1 | tests/test_crypto_intel_v6_coverage.py | Python | 830 | 2f3e13a8 |  |
| 798 | P1 | tests/test_crypto_predictor_regressions.py | Python | 209 | daa0bf5b |  |
| 799 | P1 | tests/test_cvar_notional_cap.py | Python | 142 | 8fd8fa91 |  |
| 800 | P1 | tests/test_data_duckdb_feeds.py | Python | 172 | 2d8520e8 |  |
| 801 | P1 | tests/test_data_feeds.py | Python | 187 | 1920d4fc |  |
| 802 | P1 | tests/test_data_intel_low_findings.py | Python | 205 | 35abfa2b |  |
| 803 | P1 | tests/test_decision_log_wiring.py | Python | 170 | a348027d |  |
| 804 | P1 | tests/test_decision_log_writer.py | Python | 81 | afa3c7c2 |  |
| 805 | P1 | tests/test_deploy_workflow_inputs.py | Python | 32 | 3dfd4520 |  |
| 806 | P1 | tests/test_depth_detector_v2_edges.py | Python | 135 | 0bdbfaa9 |  |
| 807 | P1 | tests/test_detector.py | Python | 538 | bfd78fe3 |  |
| 808 | P1 | tests/test_diagnostic_route_boundary.py | Python | 82 | 15394b75 |  |
| 809 | P1 | tests/test_diagnostics_instrumentation.py | Python | 152 | 9fdf13b6 |  |
| 810 | P1 | tests/test_disaster_recovery.py | Python | 67 | 7fae5b13 |  |
| 811 | P1 | tests/test_disaster_recovery_wiring.py | Python | 240 | 920a175c |  |
| 812 | P1 | tests/test_drift_gate_wiring.py | Python | 157 | 37d1a317 |  |
| 813 | P1 | tests/test_drift_integration_coverage.py | Python | 121 | 4e121733 |  |
| 814 | P1 | tests/test_duckdb_path_is_per_worker.py | Python | 64 | 0f155e82 |  |
| 815 | P1 | tests/test_ecc.py | Python | 152 | e7daca12 |  |
| 816 | P1 | tests/test_ecc_curve_boundary.py | Python | 95 | c9449358 |  |
| 817 | P1 | tests/test_ecc_node_rpc.py | Python | 195 | 8d8fb128 |  |
| 818 | P1 | tests/test_ecc_schnorr_taproot.py | Python | 128 | 16eae3a6 |  |
| 819 | P1 | tests/test_ecc_secp256k1_cluster.py | Python | 173 | f9b10a30 |  |
| 820 | P1 | tests/test_ecc_worker_pipeline.py | Python | 270 | 7754331d |  |
| 821 | P1 | tests/test_ecdsa_scan_coverage.py | Python | 128 | 997c9ce3 |  |
| 822 | P1 | tests/test_ecdsa_scanner_bounded.py | Python | 86 | 79208487 |  |
| 823 | P1 | tests/test_ed25519.py | Python | 378 | 9a3cca13 |  |
| 824 | P1 | tests/test_engine_signal_plumbing_fixes.py | Python | 151 | 011aca61 |  |
| 825 | P1 | tests/test_engines_e01_statistical.py | Python | 126 | 11b40a3e |  |
| 826 | P1 | tests/test_ensemble_blend_tuning.py | Python | 212 | 21a48168 |  |
| 827 | P1 | tests/test_ensemble_failure_semantics.py | Python | 206 | 212f0fb6 |  |
| 828 | P1 | tests/test_ensemble_predictor.py | Python | 722 | fe57bf0d |  |
| 829 | P1 | tests/test_ensemble_train_timeout.py | Python | 117 | 85944e5a |  |
| 830 | P1 | tests/test_entropy.py | Python | 126 | 4d8517ca |  |
| 831 | P1 | tests/test_env_example_documents_required_settings.py | Python | 71 | b753314c |  |
| 832 | P1 | tests/test_event_bus.py | Python | 361 | 7a4f5b8c |  |
| 833 | P1 | tests/test_event_bus_producers.py | Python | 149 | 6bf17c29 |  |
| 834 | P1 | tests/test_event_bus_producers_observability.py | Python | 449 | 4c65d24b |  |
| 835 | P1 | tests/test_event_bus_producers_remaining.py | Python | 168 | 46f506e2 |  |
| 836 | P1 | tests/test_event_loop_acquisition.py | Python | 58 | 9f6f4687 |  |
| 837 | P1 | tests/test_exec_accounting_fixes.py | Python | 200 | e5fb8d4b |  |
| 838 | P1 | tests/test_exec_idempotency_fills.py | Python | 151 | f6942dfd |  |
| 839 | P1 | tests/test_execution_cost.py | Python | 106 | 683acb8b |  |
| 840 | P1 | tests/test_execution_rl_agent.py | Python | 290 | 2a31e273 |  |
| 841 | P1 | tests/test_execution_router_coverage.py | Python | 359 | 1f942832 |  |
| 842 | P1 | tests/test_execution_router_rl_posttrade.py | Python | 216 | 9fb3e905 |  |
| 843 | P1 | tests/test_executor_fee_accounting.py | Python | 166 | 5e010a48 |  |
| 844 | P1 | tests/test_executor_residual_paths.py | Python | 334 | 7b30600a |  |
| 845 | P1 | tests/test_factor_search.py | Python | 90 | a3a7b85e |  |
| 846 | P1 | tests/test_feature_bar_gaps.py | Python | 108 | f161a476 |  |
| 847 | P1 | tests/test_feature_derivatives_nlp_tft.py | Python | 147 | a355cee7 |  |
| 848 | P1 | tests/test_feature_microstructure_mempool.py | Python | 181 | 44cc558d |  |
| 849 | P1 | tests/test_features.py | Python | 664 | 3975b3a6 |  |
| 850 | P1 | tests/test_features_mempool.py | Python | 75 | 1638304f |  |
| 851 | P1 | tests/test_features_nlp.py | Python | 154 | 92fb571d |  |
| 852 | P1 | tests/test_features_onchain.py | Python | 125 | f0b5ac42 |  |
| 853 | P1 | tests/test_fetcher_coverage.py | Python | 969 | afb9e552 |  |
| 854 | P1 | tests/test_fetcher_retry_jitter.py | Python | 97 | c46c0cc0 |  |
| 855 | P1 | tests/test_fetcher_symbol_precision.py | Python | 94 | fef0ec91 |  |
| 856 | P1 | tests/test_fetcher_venue_degradation.py | Python | 195 | 505ce832 |  |
| 857 | P1 | tests/test_folklore_gate.py | Python | 213 | 3c91b2db |  |
| 858 | P1 | tests/test_frontend_audit_scope.py | Python | 190 | 3ee1a873 |  |
| 859 | P1 | tests/test_funding_carry.py | Python | 101 | cc7256d7 |  |
| 860 | P1 | tests/test_gap015_backfill.py | Python | 394 | 1b36ebf2 |  |
| 861 | P1 | tests/test_gap015_intelligence_training.py | Python | 150 | 5f0a0cbc |  |
| 862 | P1 | tests/test_garch_unit.py | Python | 194 | 3803a805 |  |
| 863 | P1 | tests/test_gates_advisory_scalar_aggregation.py | Python | 106 | e6e333c5 |  |
| 864 | P1 | tests/test_gates_non_finite.py | Python | 273 | 6711fbaa |  |
| 865 | P1 | tests/test_gaussian_lattice.py | Python | 176 | 91e52ba7 |  |
| 866 | P1 | tests/test_github_route_contract.py | Python | 428 | 41661832 |  |
| 867 | P1 | tests/test_granger_detector.py | Python | 113 | 5e6ab530 |  |
| 868 | P1 | tests/test_greeks.py | Python | 86 | 4fa249eb |  |
| 869 | P1 | tests/test_greeks_caps_wiring.py | Python | 165 | 110864bf |  |
| 870 | P1 | tests/test_harmonic_spectral.py | Python | 164 | 18e9a936 |  |
| 871 | P1 | tests/test_hnp.py | Python | 261 | e9d9fc6b |  |
| 872 | P1 | tests/test_horizon_backfill.py | Python | 239 | bde9dded |  |
| 873 | P1 | tests/test_horizon_decision.py | Python | 153 | 7532add5 |  |
| 874 | P1 | tests/test_horizon_mlp.py | Python | 1382 | 4fc46c8c |  |
| 875 | P1 | tests/test_horizon_order_gate.py | Python | 98 | 202dbcb5 |  |
| 876 | P1 | tests/test_horizon_promotion.py | Python | 397 | 6a9b3a5d |  |
| 877 | P1 | tests/test_horizon_risk_context.py | Python | 49 | 49a2ce74 |  |
| 878 | P1 | tests/test_horizon_runtime.py | Python | 281 | 45c98138 |  |
| 879 | P1 | tests/test_horizons.py | Python | 242 | 62a918a8 |  |
| 880 | P1 | tests/test_horizons_endpoint.py | Python | 179 | e9ba0580 |  |
| 881 | P1 | tests/test_idempotency.py | Python | 449 | 064037c3 |  |
| 882 | P1 | tests/test_ingest_keeps_previous_index.py | Python | 147 | ea50b2bc |  |
| 883 | P1 | tests/test_instrumentation.py | Python | 230 | 98bd4609 |  |
| 884 | P1 | tests/test_integration_full_pipeline.py | Python | 291 | f49fa5aa |  |
| 885 | P1 | tests/test_intelligence_adapter.py | Python | 189 | 5ebab68c |  |
| 886 | P1 | tests/test_intelligence_client_coverage.py | Python | 721 | 4a9e428c |  |
| 887 | P1 | tests/test_intelligence_features_coverage.py | Python | 145 | cbdab333 |  |
| 888 | P1 | tests/test_intelligence_metrics.py | Python | 243 | 40c73454 |  |
| 889 | P1 | tests/test_intelligence_persistence.py | Python | 140 | 8843cc8d |  |
| 890 | P1 | tests/test_intelligence_providers.py | Python | 1661 | 51915cb1 |  |
| 891 | P1 | tests/test_intelligence_runtime_wiring.py | Python | 43 | d52a6e91 |  |
| 892 | P1 | tests/test_interpolation.py | Python | 120 | 674a369b |  |
| 893 | P1 | tests/test_kelly.py | Python | 828 | 6bdb8135 |  |
| 894 | P1 | tests/test_kelly_gaps.py | Python | 501 | 854b752d |  |
| 895 | P1 | tests/test_kelly_notional_cap.py | Python | 187 | 04389fe0 |  |
| 896 | P1 | tests/test_kelly_size_scalar.py | Python | 128 | d4e2d987 |  |
| 897 | P1 | tests/test_kg_assemble.py | Python | 64 | 088181c4 |  |
| 898 | P1 | tests/test_kg_db.py | Python | 46 | 3102007c |  |
| 899 | P1 | tests/test_kg_extract.py | Python | 30 | 0c00023b |  |
| 900 | P1 | tests/test_kg_ingest.py | Python | 22 | d89b5d91 |  |
| 901 | P1 | tests/test_kg_query.py | Python | 79 | 0ec21c2f |  |
| 902 | P1 | tests/test_kg_resolve.py | Python | 37 | ff9b7ea5 |  |
| 903 | P1 | tests/test_law12_cipher_suite_pattern.py | Python | 97 | a4f90962 |  |
| 904 | P1 | tests/test_live_additional_coverage.py | Python | 409 | 13f38076 |  |
| 905 | P1 | tests/test_live_executor_coverage.py | Python | 1074 | f5eb42d9 |  |
| 906 | P1 | tests/test_live_executor_fsm.py | Python | 294 | 7152c4b2 |  |
| 907 | P1 | tests/test_live_fill_quantity.py | Python | 94 | 6099f076 |  |
| 908 | P1 | tests/test_live_fsm_integration.py | Python | 164 | 38096cc5 |  |
| 909 | P1 | tests/test_live_settings.py | Python | 212 | 05dec3e5 |  |
| 910 | P1 | tests/test_lll.py | Python | 396 | fc3c3cad |  |
| 911 | P1 | tests/test_local_checks.py | Python | 64 | fb3a418a |  |
| 912 | P1 | tests/test_logging_setup.py | Python | 101 | f0decaf8 |  |
| 913 | P1 | tests/test_lowest_covered_modules.py | Python | 231 | cde4a13f |  |
| 914 | P1 | tests/test_macro_exposure_budget.py | Python | 56 | 6cea4259 |  |
| 915 | P1 | tests/test_macro_exposure_budget_check.py | Python | 96 | eaf0edf4 |  |
| 916 | P1 | tests/test_macro_exposure_wiring.py | Python | 132 | 06d72fc1 |  |
| 917 | P1 | tests/test_macro_indicators.py | Python | 126 | b8615e60 |  |
| 918 | P1 | tests/test_macro_provider_coverage.py | Python | 167 | eddb2b10 |  |
| 919 | P1 | tests/test_macro_regime.py | Python | 47 | 0f37b396 |  |
| 920 | P1 | tests/test_math_registry.py | Python | 512 | d1a14f6d |  |
| 921 | P1 | tests/test_math_strategies_audit_fixes.py | Python | 422 | 7d962559 |  |
| 922 | P1 | tests/test_mean_reversion.py | Python | 159 | af359f2b |  |
| 923 | P1 | tests/test_merge_queue_wiring.py | Python | 115 | aae98bf8 |  |
| 924 | P1 | tests/test_merkle.py | Python | 131 | a18482ab |  |
| 925 | P1 | tests/test_meta_allocator.py | Python | 163 | ecc97eaa |  |
| 926 | P1 | tests/test_meta_network_loss.py | Python | 181 | 52c11624 |  |
| 927 | P1 | tests/test_metrics.py | Python | 128 | fe796cce |  |
| 928 | P1 | tests/test_mode_persistence_atomic_failure.py | Python | 42 | 19916925 |  |
| 929 | P1 | tests/test_model_architectures.py | Python | 96 | 9784974a |  |
| 930 | P1 | tests/test_model_eval_leakage.py | Python | 249 | 3e1259aa |  |
| 931 | P1 | tests/test_model_feature_columns_by_name.py | Python | 188 | 0c6d2c0f |  |
| 932 | P1 | tests/test_model_loading_integrity.py | Python | 86 | 5279f9b5 |  |
| 933 | P1 | tests/test_model_registry.py | Python | 114 | 8cffe584 |  |
| 934 | P1 | tests/test_model_registry_promotion_gate.py | Python | 60 | 60154e3f |  |
| 935 | P1 | tests/test_model_trainer_coverage.py | Python | 1217 | 0ba5f420 |  |
| 936 | P1 | tests/test_models_gnn_head.py | Python | 41 | ff4a7fe2 |  |
| 937 | P1 | tests/test_models_gnn_head_pyg.py | Python | 46 | 5aeb6ee0 |  |
| 938 | P1 | tests/test_mongo_client_reuse.py | Python | 91 | 190bba2b |  |
| 939 | P1 | tests/test_mth020_lattice_and_pairing_cost.py | Python | 141 | 6a0153ea |  |
| 940 | P1 | tests/test_no_claude_automation.py | Python | 56 | d5c1bfe7 |  |
| 941 | P1 | tests/test_ntt.py | Python | 156 | dbe3cf15 |  |
| 942 | P1 | tests/test_numbertheory_analytics.py | Python | 287 | 5d2d0bf4 |  |
| 943 | P1 | tests/test_nutms.py | Python | 82 | 67f6f381 |  |
| 944 | P1 | tests/test_observation_boundary_contract.py | Python | 301 | a4492759 |  |
| 945 | P1 | tests/test_observation_failure.py | Python | 42 | 0d9f7362 |  |
| 946 | P1 | tests/test_observation_gate.py | Python | 207 | dd7919bf |  |
| 947 | P1 | tests/test_onchain_arkham_cryptoquant.py | Python | 222 | 3e33d989 |  |
| 948 | P1 | tests/test_onchain_base_coverage.py | Python | 363 | 9cf6718e |  |
| 949 | P1 | tests/test_onchain_no_fabricated_values.py | Python | 127 | 5e49492c |  |
| 950 | P1 | tests/test_onchain_providers_coverage.py | Python | 489 | a38f7b2c |  |
| 951 | P1 | tests/test_onchain_rate_limiter.py | Python | 141 | a3b9dd61 |  |
| 952 | P1 | tests/test_online_trainer.py | Python | 268 | 083587c3 |  |
| 953 | P1 | tests/test_online_trainer_wiring.py | Python | 312 | 155a684d |  |
| 954 | P1 | tests/test_options_carry.py | Python | 54 | 3fc82e22 |  |
| 955 | P1 | tests/test_orchestratable_safety.py | Python | 105 | 14404fbe |  |
| 956 | P1 | tests/test_orchestrator.py | Python | 302 | 9270230d |  |
| 957 | P1 | tests/test_orchestrator_allocation_rebalance.py | Python | 202 | b8991616 |  |
| 958 | P1 | tests/test_orchestrator_coverage.py | Python | 1631 | 45b269fd |  |
| 959 | P1 | tests/test_orchestrator_crypto_box_paths.py | Python | 422 | c2d3f09e |  |
| 960 | P1 | tests/test_orchestrator_extra_coverage.py | Python | 1576 | 96552bc7 |  |
| 961 | P1 | tests/test_orchestrator_pkg_planner.py | Python | 61 | 16f461f4 |  |
| 962 | P1 | tests/test_orchestrator_pkg_run.py | Python | 67 | 4593b436 |  |
| 963 | P1 | tests/test_orchestrator_pkg_synthesizer.py | Python | 24 | 886ce774 |  |
| 964 | P1 | tests/test_orchestrator_pkg_worker.py | Python | 18 | f681910b |  |
| 965 | P1 | tests/test_orchestrator_registry_publish.py | Python | 130 | 710f80f2 |  |
| 966 | P1 | tests/test_orchestrator_residual_arms.py | Python | 337 | 3bf9c521 |  |
| 967 | P1 | tests/test_orchestrator_shadow_routing.py | Python | 117 | 1f30befe |  |
| 968 | P1 | tests/test_orchestrator_strategy_correlation.py | Python | 270 | 07c7416e |  |
| 969 | P1 | tests/test_orchestrator_strategy_portfolio.py | Python | 1006 | 1368f85d |  |
| 970 | P1 | tests/test_orchestrator_trace_id.py | Python | 104 | d83d9eb2 |  |
| 971 | P1 | tests/test_order_fsm.py | Python | 448 | 7131ca04 |  |
| 972 | P1 | tests/test_order_fsm_registry.py | Python | 196 | e4be2652 |  |
| 973 | P1 | tests/test_order_fsm_transition_table.py | Python | 45 | 619dfda6 |  |
| 974 | P1 | tests/test_order_manager.py | Python | 351 | 6630c734 |  |
| 975 | P1 | tests/test_order_manager_fill_validation.py | Python | 99 | 8e2f56d2 |  |
| 976 | P1 | tests/test_order_manager_incremental_fill.py | Python | 127 | 08fbbf5b |  |
| 977 | P1 | tests/test_order_manager_log_context.py | Python | 101 | 845ae29b |  |
| 978 | P1 | tests/test_order_manager_partial_fills.py | Python | 151 | 4c2dd069 |  |
| 979 | P1 | tests/test_order_throttler.py | Python | 265 | a82e08ab |  |
| 980 | P1 | tests/test_orderbook_stream_coverage.py | Python | 259 | 538331e7 |  |
| 981 | P1 | tests/test_orderbook_stream_publish.py | Python | 179 | 3567e651 |  |
| 982 | P1 | tests/test_paper_executor.py | Python | 872 | 3bc1624e |  |
| 983 | P1 | tests/test_paper_only_timeframe_routing.py | Python | 90 | e01ca3ef |  |
| 984 | P1 | tests/test_percent_vs_fraction_units.py | Python | 105 | 37edfb9c |  |
| 985 | P1 | tests/test_performance_drift.py | Python | 582 | ded23fb2 |  |
| 986 | P1 | tests/test_performance_drift_drawdown_basis.py | Python | 102 | 47b3a849 |  |
| 987 | P1 | tests/test_performance_drift_edges.py | Python | 164 | 1c42a434 |  |
| 988 | P1 | tests/test_phase5_execution_fixes.py | Python | 208 | c9bc3f74 |  |
| 989 | P1 | tests/test_phase7_ops_findings.py | Python | 77 | 3bff132e |  |
| 990 | P1 | tests/test_portfolio_agreement.py | Python | 129 | cf44a5a2 |  |
| 991 | P1 | tests/test_portfolio_correlation.py | Python | 441 | 7a70d63a |  |
| 992 | P1 | tests/test_position_sizing.py | Python | 618 | 10e49696 |  |
| 993 | P1 | tests/test_post_trade_bounded_history.py | Python | 116 | efe91648 |  |
| 994 | P1 | tests/test_pq_transport_honesty.py | Python | 71 | 192085cb |  |
| 995 | P1 | tests/test_pr_auto_update_workflow.py | Python | 322 | 7aca0311 |  |
| 996 | P1 | tests/test_pre_tool_use_hook.py | Python | 508 | 9388a7b6 |  |
| 997 | P1 | tests/test_prfail_exact_lines.py | Python | 389 | 7fc69ed4 |  |
| 998 | P1 | tests/test_price_preview_path.py | Python | 477 | 01b18608 |  |
| 999 | P1 | tests/test_primality.py | Python | 292 | 5aa66d08 |  |
| 1000 | P1 | tests/test_prime_field.py | Python | 311 | abe47d09 |  |
| 1001 | P1 | tests/test_probabilistic_adapter.py | Python | 116 | b16f3d8c |  |
| 1002 | P1 | tests/test_probabilistic_engine.py | Python | 317 | 4b7caa08 |  |
| 1003 | P1 | tests/test_probability_consensus.py | Python | 154 | 62d07bb8 |  |
| 1004 | P1 | tests/test_prometheus_scrape_auth.py | Python | 35 | 13c1a091 |  |
| 1005 | P1 | tests/test_promotion_gauntlet.py | Python | 206 | ed1a66ea |  |
| 1006 | P1 | tests/test_promotion_gauntlet_wiring.py | Python | 201 | bd3daaaa |  |
| 1007 | P1 | tests/test_provider_basis_stale_suppression.py | Python | 109 | 1a673bb2 |  |
| 1008 | P1 | tests/test_provider_basis_sync.py | Python | 101 | 7608bef8 |  |
| 1009 | P1 | tests/test_provider_close_leak.py | Python | 77 | 733a0cf2 |  |
| 1010 | P1 | tests/test_provider_pure_logic.py | Python | 132 | 35fec4e7 |  |
| 1011 | P1 | tests/test_push_wait.py | Python | 398 | 992bd9f4 |  |
| 1012 | P1 | tests/test_quantum_margins.py | Python | 535 | f4b8fb74 |  |
| 1013 | P1 | tests/test_rag_mongo_db.py | Python | 57 | 2887ca7d |  |
| 1014 | P1 | tests/test_rag_mongo_embeddings.py | Python | 46 | a77ec316 |  |
| 1015 | P1 | tests/test_rag_mongo_generate.py | Python | 28 | c7782361 |  |
| 1016 | P1 | tests/test_rag_mongo_ingest.py | Python | 48 | ed0ffcd1 |  |
| 1017 | P1 | tests/test_rag_mongo_pipeline.py | Python | 22 | 6deb9cb9 |  |
| 1018 | P1 | tests/test_rag_mongo_retrieve.py | Python | 36 | c7c8c4c9 |  |
| 1019 | P1 | tests/test_readme_gate_list_matches_stack.py | Python | 84 | a4e7e8e0 |  |
| 1020 | P1 | tests/test_redteam_scheduler.py | Python | 54 | 05d2ee81 |  |
| 1021 | P1 | tests/test_regime_detector_v2_paths.py | Python | 125 | 9df85875 |  |
| 1022 | P1 | tests/test_regime_ensemble.py | Python | 47 | 81362b87 |  |
| 1023 | P1 | tests/test_regime_multi_init_selection.py | Python | 161 | 816c7101 |  |
| 1024 | P1 | tests/test_regime_strategy_selector.py | Python | 280 | 4c6b6a95 |  |
| 1025 | P1 | tests/test_required_import_in_ci.py | Python | 50 | ea095a7e |  |
| 1026 | P1 | tests/test_residual_gaps_batch2.py | Python | 416 | b120cc3a |  |
| 1027 | P1 | tests/test_residual_gaps_batch3.py | Python | 262 | 4b089f1b |  |
| 1028 | P1 | tests/test_residual_gaps_batch4.py | Python | 296 | ec896dea |  |
| 1029 | P1 | tests/test_residues.py | Python | 229 | c88d674d |  |
| 1030 | P1 | tests/test_resolve_registry_merge.py | Python | 100 | 7beb8e53 |  |
| 1031 | P1 | tests/test_restart_persistence.py | Python | 261 | f2ae72b7 |  |
| 1032 | P1 | tests/test_review_build_context.py | Python | 97 | 42731935 |  |
| 1033 | P1 | tests/test_review_retrieval.py | Python | 71 | 52be750e |  |
| 1034 | P1 | tests/test_rfc6979_nonces.py | Python | 178 | 0af4946b |  |
| 1035 | P1 | tests/test_risk_controls_api.py | Python | 628 | 4ccb97f8 |  |
| 1036 | P1 | tests/test_risk_gate.py | Python | 180 | 63870140 |  |
| 1037 | P1 | tests/test_risk_gates.py | Python | 413 | 1938500a |  |
| 1038 | P1 | tests/test_risk_gates_coverage.py | Python | 328 | 557dedb8 |  |
| 1039 | P1 | tests/test_risk_gates_intelligence.py | Python | 149 | 21eec210 |  |
| 1040 | P1 | tests/test_risk_pure_logic.py | Python | 332 | fc922b6e |  |
| 1041 | P1 | tests/test_risk_quantification.py | Python | 277 | c0715ef0 |  |
| 1042 | P1 | tests/test_router_fee_parsing.py | Python | 221 | 711816d4 |  |
| 1043 | P1 | tests/test_rpc_basic_auth.py | Python | 105 | 0782f493 |  |
| 1044 | P1 | tests/test_runtime_monitor_concurrent_probes.py | Python | 182 | e340073b |  |
| 1045 | P1 | tests/test_runtime_monitor_coverage.py | Python | 469 | a3efb58c |  |
| 1046 | P1 | tests/test_safe_primes.py | Python | 438 | 1d4ae1d2 |  |
| 1047 | P1 | tests/test_script_fixes_scr018.py | Python | 181 | 0bf6674c |  |
| 1048 | P1 | tests/test_scripts_path_bootstrap.py | Python | 95 | c4c1c928 |  |
| 1049 | P1 | tests/test_secp256k1.py | Python | 448 | c4cb6103 |  |
| 1050 | P1 | tests/test_security_pqc_posture.py | Python | 76 | 00928e99 |  |
| 1051 | P1 | tests/test_self_tuning_api.py | Python | 200 | 5a14228b |  |
| 1052 | P1 | tests/test_self_tuning_settings.py | Python | 30 | e6355fa6 |  |
| 1053 | P1 | tests/test_selftest_rate_limit.py | Python | 118 | b1ab3ae0 |  |
| 1054 | P1 | tests/test_settings_env_namespace.py | Python | 68 | da535ba6 |  |
| 1055 | P1 | tests/test_shadow_model_promotion.py | Python | 401 | 381394fd |  |
| 1056 | P1 | tests/test_shell_exec.py | Python | 598 | 1d75c218 |  |
| 1057 | P1 | tests/test_signal_debugger.py | Python | 350 | d8b1aed6 |  |
| 1058 | P1 | tests/test_signal_debugger_coverage.py | Python | 451 | 8a186db7 |  |
| 1059 | P1 | tests/test_signal_debugger_selftest_guards.py | Python | 67 | 38029a96 |  |
| 1060 | P1 | tests/test_signal_engine.py | Python | 1993 | 0102f884 |  |
| 1061 | P1 | tests/test_signal_engine_adapter.py | Python | 119 | b073a15f |  |
| 1062 | P1 | tests/test_signal_engine_partial_branches.py | Python | 137 | d4e3e551 |  |
| 1063 | P1 | tests/test_signal_engine_residual_paths.py | Python | 354 | 531c09d3 |  |
| 1064 | P1 | tests/test_slippage.py | Python | 183 | 5e33dbf9 |  |
| 1065 | P1 | tests/test_small_module_gaps.py | Python | 414 | 916bf762 |  |
| 1066 | P1 | tests/test_startup_readiness.py | Python | 844 | 4829f182 |  |
| 1067 | P1 | tests/test_static_invariants.py | Python | 1589 | 193b3bc9 |  |
| 1068 | P1 | tests/test_static_invariants_blind_spots.py | Python | 140 | 44ec7d50 |  |
| 1069 | P1 | tests/test_storage.py | Python | 1111 | 31dce6c8 |  |
| 1070 | P1 | tests/test_storage_write_rollback.py | Python | 102 | e5d9d7f3 |  |
| 1071 | P1 | tests/test_strategies_filters.py | Python | 628 | 1a6e0663 |  |
| 1072 | P1 | tests/test_strategy_bootstrap.py | Python | 232 | 1189a934 |  |
| 1073 | P1 | tests/test_strategy_correlation.py | Python | 113 | bcfb1913 |  |
| 1074 | P1 | tests/test_strategy_decay.py | Python | 52 | c93f7256 |  |
| 1075 | P1 | tests/test_strategy_filters.py | Python | 468 | fafe1bb8 |  |
| 1076 | P1 | tests/test_strategy_kill_switch.py | Python | 208 | aa5fdd2f |  |
| 1077 | P1 | tests/test_strategy_kill_switch_wiring.py | Python | 251 | 5a1e83cb |  |
| 1078 | P1 | tests/test_strategy_portfolio.py | Python | 781 | dfdccba9 |  |
| 1079 | P1 | tests/test_strategy_registry.py | Python | 175 | fa7a81fa |  |
| 1080 | P1 | tests/test_stress_simulator.py | Python | 138 | 6d469112 |  |
| 1081 | P1 | tests/test_stress_test_endpoint.py | Python | 168 | a7216740 |  |
| 1082 | P1 | tests/test_suite_speed_budget.py | Python | 152 | 73c584d2 |  |
| 1083 | P1 | tests/test_threshold.py | Python | 536 | 20237e4a |  |
| 1084 | P1 | tests/test_timescale_initialize_migrations.py | Python | 163 | c362dded |  |
| 1085 | P1 | tests/test_timescale_mock_coverage.py | Python | 884 | b1a60c82 |  |
| 1086 | P1 | tests/test_timescale_storage.py | Python | 1013 | 7e8749b3 |  |
| 1087 | P1 | tests/test_timescale_storage_fake_pool.py | Python | 346 | 05fc212a |  |
| 1088 | P1 | tests/test_timescaledb_script.py | Python | 138 | e966aba4 |  |
| 1089 | P1 | tests/test_tools_example_tools.py | Python | 49 | aadb0a71 |  |
| 1090 | P1 | tests/test_tools_registry.py | Python | 94 | 7df6f271 |  |
| 1091 | P1 | tests/test_trade_auditor.py | Python | 267 | bae99d09 |  |
| 1092 | P1 | tests/test_trade_journal.py | Python | 272 | a1a06f96 |  |
| 1093 | P1 | tests/test_tuning_audit.py | Python | 72 | d3c0247a |  |
| 1094 | P1 | tests/test_tuning_backtest_harness.py | Python | 517 | c59fec83 |  |
| 1095 | P1 | tests/test_tuning_bayesian_proposer.py | Python | 102 | 806c4e51 |  |
| 1096 | P1 | tests/test_tuning_bootstrap.py | Python | 298 | 89fa0043 |  |
| 1097 | P1 | tests/test_tuning_evaluator.py | Python | 208 | 37bd6396 |  |
| 1098 | P1 | tests/test_tuning_feature_window_oos.py | Python | 86 | db0701f9 |  |
| 1099 | P1 | tests/test_tuning_gate.py | Python | 94 | c99d6c66 |  |
| 1100 | P1 | tests/test_tuning_gate_multiple_testing.py | Python | 87 | 9ba0cba9 |  |
| 1101 | P1 | tests/test_tuning_live_overrides.py | Python | 212 | 637a54a0 |  |
| 1102 | P1 | tests/test_tuning_promotion_rollback_wiring.py | Python | 138 | 1b1bfbe7 |  |
| 1103 | P1 | tests/test_tuning_proposer.py | Python | 63 | a14c668d |  |
| 1104 | P1 | tests/test_tuning_registry.py | Python | 132 | 23d737c0 |  |
| 1105 | P1 | tests/test_tuning_runner.py | Python | 305 | 764f934b |  |
| 1106 | P1 | tests/test_tuning_scheduler.py | Python | 1203 | 21214898 |  |
| 1107 | P1 | tests/test_tuning_store.py | Python | 86 | 02b00855 |  |
| 1108 | P1 | tests/test_tuning_store_rollback.py | Python | 112 | eaaab96d |  |
| 1109 | P1 | tests/test_tuning_watchdog.py | Python | 181 | 55783c70 |  |
| 1110 | P1 | tests/test_tuning_watchdog_rollback_exhaustion.py | Python | 106 | b112dc12 |  |
| 1111 | P1 | tests/test_unenforced_config_knobs.py | Python | 254 | 017a68d4 |  |
| 1112 | P1 | tests/test_unified_ledger.py | Python | 74 | 1aba3c25 |  |
| 1113 | P1 | tests/test_unified_ledger_wiring.py | Python | 202 | 79f1a38e |  |
| 1114 | P1 | tests/test_universe_returns.py | Python | 281 | 8f951606 |  |
| 1115 | P1 | tests/test_upgrade_modules.py | Python | 280 | a443c429 |  |
| 1116 | P1 | tests/test_upgrade_optuna_wf.py | Python | 122 | 5d224880 |  |
| 1117 | P1 | tests/test_upgrade_optuna_wf_leakage.py | Python | 75 | c9c14466 |  |
| 1118 | P1 | tests/test_upgrade_registry.py | Python | 246 | 76980677 |  |
| 1119 | P1 | tests/test_upgrade_shadow_deploy.py | Python | 186 | 4c2280de |  |
| 1120 | P1 | tests/test_upgrade_shadow_deploy_significance.py | Python | 86 | 3264a0ed |  |
| 1121 | P1 | tests/test_venue_api.py | Python | 345 | 341d0ab2 |  |
| 1122 | P1 | tests/test_venue_controls.py | Python | 271 | 7f06c733 |  |
| 1123 | P1 | tests/test_venue_controls_api.py | Python | 220 | 2a9ad18a |  |
| 1124 | P1 | tests/test_vol_target_sizer.py | Python | 213 | 2fbf4ca2 |  |
| 1125 | P1 | tests/test_whale_gate_advisory.py | Python | 103 | f93c3d14 |  |
| 1126 | P1 | tests/test_whale_ratio_failure_path.py | Python | 77 | 4bdd41b9 |  |
| 1127 | P1 | tests/test_worker_trader.py | Python | 264 | 96403a32 |  |
| 1128 | P1 | tests/test_workers_orchestrator.py | Python | 204 | 8a5f1126 |  |
| 1129 | P1 | tests/test_workers_orchestrator_coverage.py | Python | 538 | 8ebe5d1c |  |
| 1130 | P1 | tests/test_ws_auth_query_param.py | Python | 135 | f2cf255b |  |
| 1131 | P1 | tests/test_ws_broadcaster.py | Python | 128 | b0deb4c0 |  |
| 1132 | P1 | tests/test_ws_publish_lag_metric.py | Python | 182 | c3cfea00 |  |
| 1133 | P1 | tests/test_ws_subscriptions.py | Python | 360 | 4c5214a6 |  |
| 1134 | P1 | tests/test_xsec_momentum.py | Python | 86 | 5307f89d |  |
| 1135 | P1 | tests/test_zksnark_detect_coverage.py | Python | 164 | 0f281e5c |  |
| 1136 | P1 | tests/trading/__init__.py | Python | 0 | e3b0c442 |  |
| 1137 | P1 | tests/trading/invariants/__init__.py | Python | 0 | e3b0c442 |  |
| 1138 | P1 | tests/trading/invariants/test_inv_001_max_notional.py | Python | 213 | 060fd71f |  |
| 1139 | P1 | tests/trading/invariants/test_inv_002_capital_preservation_halt.py | Python | 157 | d4e31b12 |  |
| 1140 | P1 | tests/trading/invariants/test_inv_004_non_finite.py | Python | 307 | 9906a7ce |  |
| 1141 | P1 | tests/trading/invariants/test_inv_005_disabled_mode.py | Python | 123 | 6611a4a0 |  |
| 1142 | P1 | tests/trading/invariants/test_inv_006_risk_engine_failure.py | Python | 171 | 32c8cd83 |  |
| 1143 | P2 | .agents/skills/trade-bot-code-review-pr/SKILL.md | Markdown | 23 | f7724554 |  |
| 1144 | P2 | .agents/skills/trade-bot-cookbook-engineering/SKILL.md | Markdown | 22 | 1db44afc |  |
| 1145 | P2 | .agents/skills/trade-bot-delivery/SKILL.md | Markdown | 18 | 10984afa |  |
| 1146 | P2 | .agents/skills/trade-bot-evaluation-optimization/SKILL.md | Markdown | 18 | 6a9dcbb5 |  |
| 1147 | P2 | .agents/skills/trade-bot-evidence-first/SKILL.md | Markdown | 20 | 7478d0d0 |  |
| 1148 | P2 | .agents/skills/trade-bot-openai-sdk-integration/SKILL.md | Markdown | 20 | 03900dfe |  |
| 1149 | P2 | .agents/skills/trade-bot-parallel-development/SKILL.md | Markdown | 42 | eb29101f |  |
| 1150 | P2 | .agents/skills/trade-bot-root-cause-debugging/SKILL.md | Markdown | 24 | 3918f734 |  |
| 1151 | P2 | .claude/hooks/_gh_contract.py | Python | 497 | 53c7cbc6 |  |
| 1152 | P2 | .claude/hooks/completion_gate.py | Python | 25 | 4753b1c8 |  |
| 1153 | P2 | .claude/hooks/observation_failure.py | Python | 93 | 6a2ba65b |  |
| 1154 | P2 | .claude/hooks/observation_gate.py | Python | 620 | 0d23a6ff |  |
| 1155 | P2 | .claude/hooks/pre_tool_use.py | Python | 1036 | fd662711 |  |
| 1156 | P2 | .claude/hooks/precompact_checkpoint.py | Python | 25 | d68a10de |  |
| 1157 | P2 | .claude/hooks/quality_gate.py | Python | 27 | 2c809a53 |  |
| 1158 | P2 | .claude/hooks/session-start.sh | Shell | 116 | 52bfdaa6 |  |
| 1159 | P2 | .claude/hooks/task_lifecycle.py | Python | 35 | 74f6c16a |  |
| 1160 | P2 | .claude/launch.json | JSON | 11 | 0983b089 |  |
| 1161 | P2 | .claude/settings.json | JSON | 219 | 3d486023 |  |
| 1162 | P2 | .claude/skills/crypto-architect/SKILL.md | Markdown | 420 | dd35ecc2 |  |
| 1163 | P2 | .claude/skills/crypto-architect/references/blockchain.md | Markdown | 181 | 2d70217a |  |
| 1164 | P2 | .claude/skills/crypto-architect/references/compliance.md | Markdown | 261 | bb2f02dd |  |
| 1165 | P2 | .claude/skills/crypto-architect/references/defi.md | Markdown | 235 | 27d5381e |  |
| 1166 | P2 | .claude/skills/crypto-architect/references/ecc-crypto.md | Markdown | 251 | 67fcffbf |  |
| 1167 | P2 | .claude/skills/crypto-architect/references/exchanges.md | Markdown | 195 | 6865ca93 |  |
| 1168 | P2 | .claude/skills/crypto-architect/references/market-microstructure.md | Markdown | 259 | d7443ded |  |
| 1169 | P2 | .claude/skills/crypto-architect/references/ml-models.md | Markdown | 258 | 8ac7bcef |  |
| 1170 | P2 | .claude/skills/crypto-architect/references/on-chain-data.md | Markdown | 257 | 9e09e960 |  |
| 1171 | P2 | .claude/skills/crypto-architect/references/probability.md | Markdown | 210 | ca3710b4 |  |
| 1172 | P2 | .claude/skills/crypto-architect/references/realtime-systems.md | Markdown | 284 | d5243823 |  |
| 1173 | P2 | .claude/skills/crypto-architect/references/risk.md | Markdown | 245 | 544dcc01 |  |
| 1174 | P2 | .claude/skills/crypto-architect/references/security.md | Markdown | 244 | d2af5b67 |  |
| 1175 | P2 | .claude/skills/crypto-architect/references/strategies.md | Markdown | 225 | 5e391269 |  |
| 1176 | P2 | .claude/skills/crypto-architect/scripts/validate_arch.py | Python | 1606 | b5c87009 |  |
| 1177 | P2 | .claude/skills/local-checks/SKILL.md | Markdown | 32 | e95dd706 |  |
| 1178 | P2 | .claude/skills/quality-engineering/SKILL.md | Markdown | 195 | 8e88bfd7 |  |
| 1179 | P2 | .claude/skills/quality-engineering/qe.config.json | JSON | 192 | 24789fb9 |  |
| 1180 | P2 | .claude/skills/quality-engineering/references/workflow.md | Markdown | 123 | bd0c298a |  |
| 1181 | P2 | .claude/skills/quality-engineering/schemas/change_plan.schema.json | JSON | 142 | 4acb9555 |  |
| 1182 | P2 | .claude/skills/quality-engineering/schemas/qe_config.schema.json | JSON | 121 | f560d02d |  |
| 1183 | P2 | .claude/skills/quality-engineering/scripts/qe_gate.py | Python | 488 | b333999c |  |
| 1184 | P2 | .claude/skills/quality-engineering/scripts/qe_new_requirement.py | Python | 273 | 312ae225 |  |
| 1185 | P2 | .claude/skills/quality-engineering/scripts/qe_registry_refs.py | Python | 151 | 7bbe41fa |  |
| 1186 | P2 | .codex/AUTONOMOUS_TASK_PROMPT.md | Markdown | 62 | d5d878b6 |  |
| 1187 | P2 | .codex/IMPLEMENTATION.md | Markdown | 228 | 34e220df |  |
| 1188 | P2 | .codex/agents/docs-researcher.toml | TOML | 32 | dd85dc27 |  |
| 1189 | P2 | .codex/agents/explorer.toml | TOML | 32 | c12ca20e |  |
| 1190 | P2 | .codex/agents/implementer.toml | TOML | 63 | 0563b998 |  |
| 1191 | P2 | .codex/agents/reviewer.toml | TOML | 45 | 31e5bcff |  |
| 1192 | P2 | .codex/agents/worker.toml | TOML | 46 | 08b2ffc4 |  |
| 1193 | P2 | .codex/config.toml | TOML | 7 | 6935ae7d |  |
| 1194 | P2 | .editorconfig | Text/config | 21 | 36a1d25e |  |
| 1195 | P2 | .env.example | Other text/source | 91 | 391f695f |  |
| 1196 | P2 | .gitattributes | Other text/source | 7 | 73db96a2 |  |
| 1197 | P2 | .githooks/reference-transaction | Other text/source | 10 | 28eb38fd |  |
| 1198 | P2 | .gitignore | Text/config | 50 | 4153a7d4 |  |
| 1199 | P2 | .pre-commit-config.yaml | YAML | 38 | 962e0c94 |  |
| 1200 | P2 | .python-version | Other text/source | 1 | 49a506dd |  |
| 1201 | P2 | .test_durations | Other text/source | 8977 | fa218480 |  |
| 1202 | P2 | .vscode/extensions.json | JSON | 10 | c0ffbb03 |  |
| 1203 | P2 | .vscode/settings.json | JSON | 9 | 35d5bf39 |  |
| 1204 | P2 | CONTRIBUTING.md | Markdown | 61 | 04155331 |  |
| 1205 | P2 | LICENSE | Other text/source | 21 | 49a961c5 |  |
| 1206 | P2 | SECURITY.md | Markdown | 78 | 4c96f444 |  |
| 1207 | P2 | common/__init__.py | Python | 0 | e3b0c442 |  |
| 1208 | P2 | common/claude_cli.py | Python | 79 | fbe378e7 |  |
| 1209 | P2 | common/command_schema.py | Python | 623 | c1c65a9b |  |
| 1210 | P2 | common/shell_exec.py | Python | 467 | a47d0514 |  |
| 1211 | P2 | crypto-predictor/ARCHITECTURE.md | Markdown | 251 | 0c17cd95 |  |
| 1212 | P2 | crypto-predictor/README.md | Markdown | 116 | 78148b0a |  |
| 1213 | P2 | crypto-predictor/backtest.py | Python | 188 | 50e9f598 |  |
| 1214 | P2 | crypto-predictor/data_fetch.py | Python | 74 | cde705ee |  |
| 1215 | P2 | crypto-predictor/data_fetch_kraken.py | Python | 55 | 72e74d38 |  |
| 1216 | P2 | crypto-predictor/indicators.py | Python | 109 | 0c688cf6 |  |
| 1217 | P2 | crypto-predictor/risk.py | Python | 98 | f0ae604b |  |
| 1218 | P2 | crypto-predictor/validation.py | Python | 127 | 43336585 |  |
| 1219 | P2 | crypto-predictor/volatility.py | Python | 84 | bf46ec4a |  |
| 1220 | P2 | docs/agents/OPENAI_COOKBOOK_ADOPTION.md | Markdown | 41 | 7c9a78f0 |  |
| 1221 | P2 | docs/next_plan_findings.md | Markdown | 21 | 620b7b2a |  |
| 1222 | P2 | docs/security/ci-diagnostics.md | Markdown | 145 | c8b8f61a |  |
| 1223 | P2 | frontend/.nvmrc | Text/config | 1 | f14b4987 |  |
| 1224 | P2 | frontend/browser-e2e/dashboard.e2e.jsx | React JSX | 360 | ea0f5239 |  |
| 1225 | P2 | frontend/electron/main.cjs | CommonJS | 185 | afcd257f |  |
| 1226 | P2 | frontend/electron/preload.cjs | CommonJS | 28 | 5b584536 |  |
| 1227 | P2 | frontend/electron/security.cjs | Other text/source | 64 | 2dcefbc6 |  |
| 1228 | P2 | frontend/electron/terminalBridge.cjs | CommonJS | 230 | fadfbaff |  |
| 1229 | P2 | frontend/index.html | HTML | 14 | 937890f7 |  |
| 1230 | P2 | frontend/linux/tradebot-dashboard.desktop | Desktop-entry config | 9 | d8c53c4f |  |
| 1231 | P2 | frontend/package-lock.json | JSON | 4854 | dd172379 |  |
| 1232 | P2 | frontend/postcss.config.js | JavaScript | 7 | ad943233 |  |
| 1233 | P2 | frontend/public/icon.svg | Vector asset | 15 | 9a6da623 |  |
| 1234 | P2 | frontend/scripts/build-icons.mjs | ES module | 36 | 4489c079 |  |
| 1235 | P2 | frontend/scripts/install-desktop-shortcut.sh | Shell | 86 | 6a03fdd9 |  |
| 1236 | P2 | frontend/src/approvals.js | JavaScript | 9 | a282face |  |
| 1237 | P2 | frontend/src/approvals.test.js | JavaScript | 17 | cf00b67c |  |
| 1238 | P2 | frontend/src/buildGuard.js | JavaScript | 57 | 1a9b0dc3 |  |
| 1239 | P2 | frontend/src/components/Controls.test.jsx | React JSX | 106 | cf6f9c5a |  |
| 1240 | P2 | frontend/src/components/ErrorBoundary.jsx | React JSX | 33 | 4ffb65c6 |  |
| 1241 | P2 | frontend/src/components/panels/ControlHubPanel.test.jsx | React JSX | 50 | b321eca5 |  |
| 1242 | P2 | frontend/src/security/frontendSecurity.test.jsx | React JSX | 108 | 1b269f1b |  |
| 1243 | P2 | frontend/tailwind.config.js | JavaScript | 43 | a8d2f444 |  |
| 1244 | P2 | frontend/vite.config.js | JavaScript | 43 | 82982458 |  |
| 1245 | P2 | frontend/vitest.browser.config.js | JavaScript | 19 | 968832f5 |  |
| 1246 | P2 | frontend/vitest.config.js | JavaScript | 14 | d37c0445 |  |
| 1247 | P2 | kg/__init__.py | Python | 0 | e3b0c442 |  |
| 1248 | P2 | kg/assemble.py | Python | 48 | 991327ed |  |
| 1249 | P2 | kg/config.py | Python | 12 | 02f60bb4 |  |
| 1250 | P2 | kg/db.py | Python | 39 | 29dd8727 |  |
| 1251 | P2 | kg/extract.py | Python | 21 | c97eece2 |  |
| 1252 | P2 | kg/ingest.py | Python | 9 | 34d740a2 |  |
| 1253 | P2 | kg/query.py | Python | 55 | 5ad9efb1 |  |
| 1254 | P2 | kg/resolve.py | Python | 30 | 2277a38a |  |
| 1255 | P2 | kg/schema.py | Python | 42 | 86f3afdb |  |
| 1256 | P2 | kg_cli.py | Python | 30 | e83e37da |  |
| 1257 | P2 | orchestrator/__init__.py | Python | 0 | e3b0c442 |  |
| 1258 | P2 | orchestrator/config.py | Python | 15 | b9451580 |  |
| 1259 | P2 | orchestrator/planner.py | Python | 47 | 3c48142f |  |
| 1260 | P2 | orchestrator/run.py | Python | 67 | 2d6754d1 |  |
| 1261 | P2 | orchestrator/synthesizer.py | Python | 18 | 3f5f44bf |  |
| 1262 | P2 | orchestrator/worker.py | Python | 27 | a4668aae |  |
| 1263 | P2 | orchestrator_cli.py | Python | 16 | 1817eda3 |  |
| 1264 | P2 | rag_cli.py | Python | 39 | 47b9e6bf |  |
| 1265 | P2 | rag_mongo/__init__.py | Python | 0 | e3b0c442 |  |
| 1266 | P2 | rag_mongo/config.py | Python | 14 | da9922ab |  |
| 1267 | P2 | rag_mongo/db.py | Python | 80 | 0a1ac336 |  |
| 1268 | P2 | rag_mongo/embeddings.py | Python | 21 | 9635c55e |  |
| 1269 | P2 | rag_mongo/generate.py | Python | 19 | 2eaea14b |  |
| 1270 | P2 | rag_mongo/ingest.py | Python | 21 | b3d1dff7 |  |
| 1271 | P2 | rag_mongo/pipeline.py | Python | 7 | b445a01a |  |
| 1272 | P2 | rag_mongo/retrieve.py | Python | 20 | 553da338 |  |
| 1273 | P2 | requirements-topology-optional.txt | Text | 9 | 69f74fd0 |  |
| 1274 | P2 | review/__init__.py | Python | 0 | e3b0c442 |  |
| 1275 | P2 | review/build_context.py | Python | 75 | 3de69e47 |  |
| 1276 | P2 | review/config.py | Python | 8 | b6dbb57a |  |
| 1277 | P2 | review/retrieval.py | Python | 60 | 9c4e1629 |  |
| 1278 | P2 | tools/__init__.py | Python | 0 | e3b0c442 |  |
| 1279 | P2 | tools/example_tools.py | Python | 50 | bf4d6a53 |  |
| 1280 | P2 | tools/registry.py | Python | 114 | c3a96723 |  |
