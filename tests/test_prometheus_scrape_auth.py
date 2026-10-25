"""REG-1608: Prometheus authenticates its /metrics scrape (audit OPS-013).

The scrape config used to carry its auth commented out, with a note pointing
at a proxy that "strips the header check" -- which would serve /metrics,
equity values included, to anyone on the network. The API accepts only the
``X-API-Key`` header, and Prometheus 2.55+ can send it through
``http_headers``; the key comes from a mounted file, never from the repo.

Decides: REG-1608"""

from __future__ import annotations

from pathlib import Path

import yaml

CONFIG = Path(__file__).resolve().parents[1] / "deploy" / "prometheus.yml"


def _api_job() -> dict:
    jobs = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))["scrape_configs"]
    (job,) = [j for j in jobs if j.get("metrics_path") == "/metrics"]
    return job


def test_the_api_scrape_sends_the_api_key_header_from_a_file() -> None:
    headers = {name.lower(): spec for name, spec in _api_job().get("http_headers", {}).items()}
    assert "x-api-key" in headers, "the /metrics scrape sends no X-API-Key"
    spec = headers["x-api-key"]
    assert spec.get("files"), "the key must come from a mounted file"
    assert "values" not in spec and "secrets" not in spec, "no key material in the repo"


def test_the_config_no_longer_recommends_stripping_the_check() -> None:
    assert "strips the header check" not in CONFIG.read_text(encoding="utf-8")
