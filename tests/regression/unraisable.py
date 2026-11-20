"""REG-1707: catch exceptions raised by finalizers that no test can catch."""

from __future__ import annotations

import gc
import sys
from typing import Any


def collect_unraisable() -> list[Any]:
    """Collect cyclic garbage and return every exception its finalizers raised."""
    caught: list[Any] = []
    previous = sys.unraisablehook
    sys.unraisablehook = caught.append
    try:
        gc.collect()
    finally:
        sys.unraisablehook = previous
    return caught
