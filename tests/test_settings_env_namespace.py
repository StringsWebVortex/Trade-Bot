"""Every environment variable feeds exactly one settings field (API-031, REG-1703).

StrategyPortfolioSettings and StrategySettings both read ``env_prefix="STRATEGY_"``.
Their field names are disjoint today, so the shared prefix is harmless. A later
field added to one class under a name the other already uses would make one
environment variable bind both models, with nothing raised: the operator sets a
knob for one strategy layer and silently moves the other as well.

This test makes that collision fail the build instead of passing unnoticed. It
covers every sub-settings class composed into Settings, and the root Settings
fields themselves (no prefix), because a prefixed nested name can equally
collide with a root name.
"""

from __future__ import annotations

from collections import defaultdict

from pydantic_settings import BaseSettings

from src.config import Settings, StrategyPortfolioSettings, StrategySettings


def _env_names(model: type[BaseSettings]) -> dict[str, str]:
    """Upper-cased env var name -> field name, as pydantic-settings resolves it."""
    prefix = str(model.model_config.get("env_prefix", "") or "")
    names: dict[str, str] = {}
    for field_name, info in model.model_fields.items():
        # A validation alias replaces prefix+name as the env lookup key.
        alias = info.validation_alias
        key = alias if isinstance(alias, str) else f"{prefix}{field_name}"
        names[key.upper()] = field_name
    return names


def _settings_classes() -> list[type[BaseSettings]]:
    classes: list[type[BaseSettings]] = [Settings]
    for info in Settings.model_fields.values():
        annotation = info.annotation
        if (
            isinstance(annotation, type)
            and issubclass(annotation, BaseSettings)
            and annotation not in classes
        ):
            classes.append(annotation)
    return classes


def test_the_two_strategy_classes_share_a_prefix_but_no_field() -> None:
    portfolio = _env_names(StrategyPortfolioSettings)
    strategy = _env_names(StrategySettings)
    assert set(portfolio) & set(strategy) == set()


def test_no_env_var_binds_two_settings_fields() -> None:
    owners: dict[str, list[str]] = defaultdict(list)
    for model in _settings_classes():
        for env_name, field_name in _env_names(model).items():
            owners[env_name].append(f"{model.__name__}.{field_name}")
    collisions = {name: fields for name, fields in owners.items() if len(fields) > 1}
    assert collisions == {}


def test_both_strategy_classes_are_composed_into_settings() -> None:
    """The guard above is vacuous unless it actually walks both classes."""
    classes = _settings_classes()
    assert StrategyPortfolioSettings in classes
    assert StrategySettings in classes
