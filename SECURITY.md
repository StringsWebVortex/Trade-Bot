# Security Policy

## Reporting a vulnerability

Report suspected vulnerabilities privately through GitHub's
[Report a vulnerability](https://github.com/zulqarnain106612-cpu/Trade-Bot/security/advisories/new)
form. Please do not open a public issue for anything exploitable.

Include the affected version or commit, reproduction steps, and the impact you
believe it has. Expect an initial response within seven days.

## Scope

This repository is trading software: it holds exchange API keys and can place
orders. Treat the following as security-relevant, not merely bugs:

- Anything that leaks credentials, API keys, or private keys — including into
  logs, metrics, error messages, or URLs.
- Anything that lets an untrusted input reach an order-placement path, or that
  bypasses the risk gates and kill switches.
- Anything that silently degrades a safety signal instead of failing loudly.

## Security review guidelines

Automated reviewers (ChatGPT Codex code and security review, GitHub Copilot
code review, CodeQL) and human reviewers should treat the following as
security findings on any pull request. `AGENTS.md` ("Code Review Rules")
lists the wider review rules, and `docs/security/THREAT_MODEL.md` is the
threat model.

- Secrets: credentials, exchange keys, JWTs, database passwords, or
  authorization headers written to source, logs, exceptions, API responses,
  metrics, URLs, test output, Docker images, frontend bundles, or workflow
  YAML. Secrets belong in ignored local env files, GitHub environment secrets
  or OIDC, and a secret manager in production.
- Order path: untrusted input reaching order placement or sizing; live trading
  reachable from defaults or tests; a risk gate, kill switch, halt, or operator
  approval that fails open.
- API: FastAPI or WebSocket routes missing authentication, authorization,
  input validation, or rate limiting; IDOR, injection, or SSRF.
- Cryptography: custom algorithms, non-constant-time secret comparison,
  non-CSPRNG randomness for tokens or keys, disabled TLS verification, or
  signed requests that accept modified or replayed payloads.
- Supply chain: GitHub Actions not pinned to a full SHA, broadened workflow
  `permissions`, production secrets exposed to pull-request jobs, or a workflow
  that invokes an AI agent unattended.
- Agent control plane: changes to `.claude/hooks/`, `.claude/settings.json`,
  `config/command_policy.json`, `config/observation_boundary.json`,
  `common/command_schema.py`, or `src/agent_control/` that widen what an agent
  can run or read. These paths require owner review.

Every confirmed security finding gets a permanent `SEC-` entry in
`config/quality_registry.json` and a deciding test, and that test is never
removed once the finding is fixed.

## Engineering policy

The threat model, key management, incident response, and the full security
engineering policy live in `docs/security/`:

- `docs/security/SECURITY_POLICY.md`
- `docs/security/THREAT_MODEL.md`
- `docs/security/KEY_MANAGEMENT.md`
- `docs/security/INCIDENT_RESPONSE.md`

## Supported versions

Only `main` receives security fixes. There are no maintained release branches.

## Automated scanning

CodeQL (`security-and-quality`) runs on every pull request and weekly on a
schedule; Dependabot opens grouped dependency updates weekly.
`.github/workflows/security.yml` runs Bandit, pip-audit, npm audit, TruffleHog,
dependency review, the supply-chain posture checks, and a container scan on
every pull request and in the merge queue.
