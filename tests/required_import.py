"""Import a dependency that a test needs, skipping only outside CI (TSA-07).

``pytest.importorskip`` turns a missing dependency into a skip. Locally that is
a convenience; in CI it means a broken install silently switches off a
security or quality test and the job still goes green. GitHub Actions sets
``CI``, so there the import is a plain one and a missing module fails
collection instead.
"""

from __future__ import annotations

import importlib
import os
from types import ModuleType

import pytest


def require(name: str) -> ModuleType:
    if os.environ.get("CI"):
        return importlib.import_module(name)
    return pytest.importorskip(name)
