# Codex setup for Trade-Bot

This repository supports Codex through root AGENTS.md and repository-local skills. Codex CLI and the VS Code extension share local Codex configuration. Project settings are applied only after the repository is trusted in the Codex client.

## Included configuration

- AGENTS.md: repository engineering contract for Codex; directs the agent to the more detailed existing CLAUDE.md and repository governance.
- .agents/skills/: reusable repository-specific evidence-first, delivery, implementation, debugging, parallel agent/sub-agent coordination, OpenAI SDK, and evaluation/optimization workflows.
- .vscode/extensions.json: recommends the official OpenAI ChatGPT/Codex extension alongside the repository's existing extensions.

## Codex CLI and VS Code

1. Install/update the official Codex CLI only if you intend to use the terminal interface; the VS Code extension can run without a separately installed codex command. Sign in through the supported Codex account flow. Do not place API keys or OAuth tokens in this repository.
2. Open this repository in VS Code and trust it only if you intend to run its code and project settings. Open the Codex extension, start a new session, and verify that it picks up the repository instructions.
3. Skills are in .agents/skills/. Invoke them explicitly by name when useful, or let Codex select them from their descriptions.

## OpenAI Cookbook patterns

See [OPENAI_COOKBOOK_ADOPTION.md](OPENAI_COOKBOOK_ADOPTION.md) for the source-pinned map from relevant Cookbook recipes to Trade-Bot skills and engineering boundaries. We adopt relevant patterns rather than copying the entire Cookbook. In particular, no LLM or OpenAI SDK is inserted into the deterministic trading/risk path by this skills/configuration change.

## Developer platform / Build with Codex

Repository configuration does not create a developer-platform project, enable API billing, create an API key, or configure account-level Build with Codex features. If you separately build an API-powered Codex integration or use the official Codex GitHub Action, create the needed platform project and secret in the appropriate account UI. Store credentials as local ignored environment values or GitHub Actions secrets (for example, OPENAI_API_KEY); never commit them or copy them into agent prompts. Codex CLI signed in through ChatGPT does not require this repository to contain an API key.

## Pull request review and handoff (ChatGPT Codex in GitHub)

Claude opens a pull request and then leaves it alone; ChatGPT Codex carries it to merge (GOV-067, CLAUDE.md section 10). The repository side is:

- `AGENTS.md` "Code Review Rules": what Codex code review (and GitHub Copilot code review, which also reads the root `AGENTS.md`) flags as P0/P1.
- `AGENTS.md` "Pull request handoff": what Codex may and may not do when asked to fix a pull request.
- `SECURITY.md` "Security review guidelines" and `docs/security/THREAT_MODEL.md`: security review context.
- `.github/workflows/codex-pr-handoff.yml` with `scripts/codex_pr_handoff.py`: comments `@codex fix ...` when CI, CodeQL, Security or Workflow lint fails on the current head, or when a Codex review leaves inline findings. Once per head, at most five times per pull request, then one notice and nothing more. It does nothing until it is on `main`.
- `scripts/codex_setup.sh`: the Codex cloud environment setup script.

One-time setup outside the repository:

1. ChatGPT Codex settings, Code review, this repository: Automatic review on. Optionally turn on Auto security review and point its threat model at `docs/security/THREAT_MODEL.md`.
2. ChatGPT Codex environment for this repository: set the setup script to `bash scripts/codex_setup.sh`. Add no exchange or production credentials.
3. Allow the Codex GitHub connector to push to pull request branches in this repository.
4. Create a fine-grained personal access token for this repository only, with Pull requests and Issues read and write, and store it as the Actions secret `CODEX_HANDOFF_TOKEN`. Codex acts on `@codex` comments from a person with Codex access, so the comments are posted as you. Without the secret the workflow fails and posts nothing.
5. Arm auto-merge (squash) on each pull request when you accept it. Nothing in this setup merges or arms auto-merge.
