"""REG-1605: the LLL and pairing references no longer redo work they can update (MTH-020).

* ``lll_reduce_with_transform`` recomputed the full Fraction Gram-Schmidt after
  every size reduction. It now updates ``mu`` in place, which is exact, so its
  steps -- and therefore its output and transform -- are those of the old
  algorithm, with one Gram-Schmidt per outer iteration instead of one per
  reduction.
* ``integer_lll_reduce`` ran a full Fraction Gram-Schmidt up front only to
  detect a dependent basis -- the slow path it exists to avoid. It now reads a
  zero integer Gram determinant instead, with the same error.
* The pairing raised the Miller output to ``(p^12 - 1) / r`` directly. It now
  takes the easy part through the Frobenius map and only exponentiates by
  ``(p^4 - p^2 + 1) / r``; the result is the same field element.

Decides: REG-1605"""

from __future__ import annotations

import random
import sys
from fractions import Fraction

import pytest

from src.mathcore.curves import bls12_381
from src.mathcore.lattice import lll
from src.mathcore.lattice.lll import DEFAULT_DELTA, gram_schmidt

_GRAM_SCHMIDT = gram_schmidt


def _reference_with_transform(basis: list[list[int]]) -> tuple[list[list[int]], list[list[int]]]:
    """The pre-MTH-020 loop, recomputing Gram-Schmidt after every reduction."""
    rows = [list(row) for row in basis]
    n = len(rows)
    transform = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    k = 1
    while k < n:
        orthogonal, mu = gram_schmidt(rows)
        for j in range(k - 1, -1, -1):
            if abs(mu[k][j]) > Fraction(1, 2):
                factor = lll._nearest_integer(mu[k][j])
                rows[k] = [a - factor * b for a, b in zip(rows[k], rows[j], strict=True)]
                transform[k] = [
                    a - factor * b for a, b in zip(transform[k], transform[j], strict=True)
                ]
                orthogonal, mu = gram_schmidt(rows)
        left = lll._dot(orthogonal[k], orthogonal[k])
        right = (DEFAULT_DELTA - mu[k][k - 1] ** 2) * lll._dot(orthogonal[k - 1], orthogonal[k - 1])
        if left >= right:
            k += 1
        else:
            rows[k], rows[k - 1] = rows[k - 1], rows[k]
            transform[k], transform[k - 1] = transform[k - 1], transform[k]
            k = max(k - 1, 1)
    return rows, transform


def _independent_bases(seed: str, dimension: int, count: int) -> list[list[list[int]]]:
    rng = random.Random(seed)
    bases: list[list[list[int]]] = []
    while len(bases) < count:
        basis = [[rng.randint(-60, 60) for _ in range(dimension)] for _ in range(dimension)]
        try:
            gram_schmidt(basis)
        except ValueError:
            continue
        bases.append(basis)
    return bases


@pytest.mark.parametrize("dimension", [3, 6])
def test_the_in_place_update_takes_the_same_steps(dimension: int) -> None:
    for basis in _independent_bases(f"mth020-{dimension}", dimension, 5):
        assert lll.lll_reduce_with_transform(basis) == _reference_with_transform(basis)


def _count_gram_schmidt(monkeypatch: pytest.MonkeyPatch, module: object, run) -> int:
    calls = [0]

    def counting(rows):
        calls[0] += 1
        return _GRAM_SCHMIDT(rows)

    with monkeypatch.context() as patch:
        patch.setattr(module, "gram_schmidt", counting)
        run()
    return calls[0]


def test_size_reduction_no_longer_recomputes_gram_schmidt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    (basis,) = _independent_bases("mth020-count", 6, 1)
    new = _count_gram_schmidt(monkeypatch, lll, lambda: lll.lll_reduce_with_transform(basis))
    this_module = sys.modules[__name__]
    old = _count_gram_schmidt(monkeypatch, this_module, lambda: _reference_with_transform(basis))
    assert new < old


def test_integer_lll_never_builds_a_fraction_gram_schmidt(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    def refuse(rows):
        raise AssertionError("integer_lll_reduce ran the Fraction Gram-Schmidt")

    monkeypatch.setattr(lll, "gram_schmidt", refuse)
    (basis,) = _independent_bases("mth020-int", 8, 1)
    reduced = lll.integer_lll_reduce(basis)
    monkeypatch.undo()
    assert lll.is_lll_reduced(reduced)


@pytest.mark.parametrize(
    ("basis", "row"),
    [
        ([[0, 0], [1, 0]], 0),
        ([[1, 2], [2, 4]], 1),
        ([[1, 2, 3], [0, 1, 0], [1, 3, 3]], 2),
    ],
)
def test_integer_lll_names_the_dependent_row(basis: list[list[int]], row: int) -> None:
    with pytest.raises(ValueError, match=f"row {row} is a linear combination"):
        lll.integer_lll_reduce(basis)


@pytest.fixture(scope="module")
def fp12_element() -> bls12_381.FQP:
    rng = random.Random("mth020-fp12")
    return bls12_381.FQ12([rng.randrange(bls12_381.FIELD_MODULUS) for _ in range(12)])


def test_frobenius_is_the_p_th_power(fp12_element: bls12_381.FQP) -> None:
    assert bls12_381._frobenius(fp12_element) == fp12_element**bls12_381.FIELD_MODULUS


def test_the_split_final_exponentiation_equals_the_direct_one(
    fp12_element: bls12_381.FQP,
) -> None:
    p, r = bls12_381.FIELD_MODULUS, bls12_381.CURVE_ORDER
    assert bls12_381._final_exponentiation(fp12_element) == fp12_element ** ((p**12 - 1) // r)
