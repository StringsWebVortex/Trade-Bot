#!/usr/bin/env bash
# Setup script for the ChatGPT Codex cloud environment (GOV-067).
#
# Paste `bash scripts/codex_setup.sh` into the environment's setup script in
# ChatGPT Codex settings. It mirrors the CI test install: CPU-only torch first,
# so the CUDA wheel is never downloaded, then the runtime and dev requirements.
# No credentials are needed or used.
set -euo pipefail

python3 -m pip install --upgrade pip uv
# Keep both installs in step with the python-tests job in .github/workflows/ci.yml.
uv pip install --system --index-url https://download.pytorch.org/whl/cpu "torch>=2.14.0,<3.0"
uv pip install --system -r requirements.txt -r requirements-dev.txt
