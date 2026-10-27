"""GOV-070 self-test fixture: one test that fails on purpose.

Not collected by the suite (the name does not start with test_); only
`./scripts/problems selftest pytest` runs it, by path.
"""


def test_a_failing_assertion_is_reported_at_its_line() -> None:
    assert 1 == 2


def test_a_passing_test_prints_nothing() -> None:
    assert 1 == 1
