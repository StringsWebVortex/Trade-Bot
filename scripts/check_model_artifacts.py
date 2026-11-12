#!/usr/bin/env python3
"""
Model-artifact preflight.

Reads ``StorageSettings.model_dir`` and reports, per active timeframe, whether
a model bundle looks present on disk. The orchestrator's startup path will
train initial models automatically if none are present, but training on a
fresh checkout can take a very long time — this script gives an operator a
fast "is anything there?" answer before starting the loop.

Exit codes:
    0  every active timeframe has at least one artifact file under model_dir
    1  one or more timeframes have no artifact — training will run on boot
    2  bad configuration (model_dir missing / unreadable)

This is a heuristic. It does not verify manifest signatures — that runs
inside src/models/trainer.py's ``_verify_manifest`` on load.
"""

from __future__ import annotations

import sys
from pathlib import Path

# Run as `python scripts/check_model_artifacts.py` and it is scripts/ that lands on
# sys.path, not the repo root, so the first-party imports below do not
# resolve on their own. Anchoring on __file__ rather than the cwd keeps
# that true from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.config import get_settings  # noqa: E402

_ARTIFACT_PATTERNS = ("xgb_direction_*_{tf}.joblib", "xgb_meta_*_{tf}.joblib")


def _artifacts_for(model_dir: Path, tf: str) -> list[Path]:
    # Match the trainer's exact names. A substring match let "*5m*" match the
    # 15m artifacts, so the 5m preflight reported OK with no 5m model on disk.
    found: list[Path] = []
    for pattern in _ARTIFACT_PATTERNS:
        found.extend(p for p in model_dir.rglob(pattern.format(tf=tf)) if p.is_file())
    return found


def main() -> int:
    settings = get_settings()
    model_dir: Path = settings.storage.model_dir

    if not model_dir.exists():
        print(
            f"[FAIL] model_dir does not exist: {model_dir}\n"
            "       Startup will create it and train from scratch.",
            file=sys.stderr,
        )
        return 2

    if not model_dir.is_dir():
        print(f"[FAIL] model_dir is not a directory: {model_dir}", file=sys.stderr)
        return 2

    all_present = True
    for tf in settings.active_timeframes:
        # Trainer naming convention: files under model_dir contain the
        # timeframe value in their name (see src/models/trainer.py save
        # paths). A missing timeframe means startup will retrain it.
        matches = _artifacts_for(model_dir, tf.value)
        if matches:
            print(f"[ OK ] {tf.value}: {len(matches)} file(s)")
        else:
            print(f"[MISS] {tf.value}: no artifacts under {model_dir}")
            all_present = False

    return 0 if all_present else 1


if __name__ == "__main__":
    sys.exit(main())
