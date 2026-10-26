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
