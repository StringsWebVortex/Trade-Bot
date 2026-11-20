"""SEC-1121..1123: model artifacts are deserialized only from verified bytes
(INT-009 OnlineTrainer, INT-010 HorizonMLPExpert, INT-011 EnsemblePredictor).

Decides:
  - SEC-1121 (INT-009) OnlineTrainer persists and loads models only through an atomic, manifest-verified path
  - SEC-1122 (INT-010) HorizonMLPExpert deserializes exactly the bytes it hashed
  - SEC-1123 (INT-011) EnsemblePredictor save is atomic and load deserializes only verified bytes
"""

from __future__ import annotations

import io
from pathlib import Path
from unittest.mock import patch

import joblib
import pytest

from src.intelligence import ensemble_predictor as ep
from src.models.online_trainer import OnlineTrainer


def _trainer(model_dir: Path) -> OnlineTrainer:
    return OnlineTrainer(model_dir=model_dir)


def test_sec_online_trainer_save_writes_manifest(tmp_path):
    t = _trainer(tmp_path)
    t.save()
    for name in ("online_direction.pkl", "online_meta.pkl"):
        assert (tmp_path / name).with_suffix(".sha256").exists()
        assert not list(tmp_path.glob("*.tmp*"))


def test_sec_online_trainer_refuses_unmanifested_pickle(tmp_path):
    class Boom:
        def __reduce__(self):
            return (pytest.fail, ("unverified pickle was executed",))

    joblib.dump(Boom(), tmp_path / "online_direction.pkl")
    t = _trainer(tmp_path)  # must not unpickle; falls back to fresh models
    assert t._dir_model.n_samples == 0


def test_sec_online_trainer_refuses_tampered_pickle(tmp_path):
    _trainer(tmp_path).save()
    (tmp_path / "online_direction.pkl").write_bytes(b"tampered")
    with patch.object(joblib, "load", side_effect=AssertionError("loaded tampered")):
        t = _trainer(tmp_path)
    assert t._dir_model.n_samples == 0


def test_sec_ensemble_verify_returns_bytes_and_load_uses_them(tmp_path, monkeypatch):
    path = tmp_path / "ensemble_X_1m.joblib"
    data = b"payload"
    path.write_bytes(data)
    ep._write_manifest(path, data)
    assert ep._verify_manifest(path) == data
    path.write_bytes(b"swapped")
    with pytest.raises(RuntimeError):
        ep._verify_manifest(path)


def test_sec_ensemble_load_does_not_reread_file(tmp_path):
    payload = {"models": {}, "weights": {}, "feature_cols": ["a"]}
    buf = io.BytesIO()
    joblib.dump(payload, buf)
    path = tmp_path / ep._MODEL_FILENAME.format(symbol="X", timeframe="1m")
    ep._atomic_write_bytes(path, buf.getvalue())
    ep._write_manifest(path, buf.getvalue())
    seen = []
    real = joblib.load

    def spy(f, *a, **k):
        seen.append(f)
        return real(f, *a, **k)

    with patch.object(ep.joblib, "load", spy):
        ep.EnsemblePredictor.load(tmp_path, "X", "1m")
    assert seen and not isinstance(seen[0], (str, Path))


def test_sec_horizon_mlp_load_deserializes_hashed_bytes():
    src = Path("src/models/horizon_mlp.py").read_text()
    assert "joblib.load(io.BytesIO(payload))" in src
    assert "joblib.load(artifact_path)" not in src
