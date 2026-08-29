"""
Shared YAML config loader for pipeline.py, training.sft.train, training.rlvr.train.

Resolution priority (highest first):
    1. CLI flags explicitly provided on the command line
    2. Values from --config <path>.yaml (under the script's section)
    3. Dataclass defaults

Usage from each entry point:

    from training.common.config_loader import load_config_for_section

    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default=None)
    # ... other flags, all with default=None ...
    args = parser.parse_args()

    cfg = load_config_for_section(
        cfg_class=PipelineConfig,
        section="pipeline",
        config_path=args.config,
        cli_namespace=args,
    )
"""

from __future__ import annotations

from dataclasses import fields, is_dataclass
from pathlib import Path
from typing import Any, TypeVar

import yaml

T = TypeVar("T")


def _read_yaml(path: str | Path) -> dict:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Config file not found: {p}")
    with open(p, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if data is None:
        return {}
    if not isinstance(data, dict):
        raise ValueError(
            f"Top-level YAML in {p} must be a mapping, got {type(data).__name__}"
        )
    return data


def _coerce(value: Any, target: Any) -> Any:
    """
    Best-effort coerce a YAML/CLI value to the type implied by `target`
    (the dataclass default). Lists and bools are handled explicitly.
    """
    if value is None:
        return None
    if isinstance(target, bool):
        if isinstance(value, bool):
            return value
        if isinstance(value, str):
            return value.strip().lower() in ("1", "true", "yes", "y", "on")
        return bool(value)
    if isinstance(target, list):
        if isinstance(value, list):
            return list(value)
        return [value]
    if isinstance(target, int) and not isinstance(target, bool):
        return int(value)
    if isinstance(target, float):
        return float(value)
    if isinstance(target, str):
        return str(value)
    return value


def load_config_for_section(
    cfg_class: type[T],
    section: str,
    config_path: str | None,
    cli_namespace: Any,
) -> T:
    """
    Build a populated dataclass instance using the priority rules above.

    `cfg_class` must be a dataclass with a no-arg constructor that yields
    the canonical defaults.

    `cli_namespace` is the argparse Namespace; only attributes whose value
    is *not None* are treated as explicit CLI overrides (this is why each
    argparse flag must be registered with `default=None`).
    """
    if not is_dataclass(cfg_class):
        raise TypeError(f"{cfg_class!r} must be a dataclass")

    cfg = cfg_class()  # type: ignore[call-arg]
    field_map = {f.name: f for f in fields(cfg)}

    # --- Step 1: overlay YAML values (skipping unknown keys) ---
    if config_path:
        raw = _read_yaml(config_path)
        section_data = raw.get(section, {}) or {}
        if not isinstance(section_data, dict):
            raise ValueError(
                f"Config section '{section}' in {config_path} must be a mapping, "
                f"got {type(section_data).__name__}"
            )
        unknown = set(section_data) - set(field_map)
        if unknown:
            # Don't fail hard — just warn through stderr-ish path.
            import sys

            print(
                f"[config] Warning: ignoring unknown keys in [{section}]: "
                f"{sorted(unknown)}",
                file=sys.stderr,
            )
        for name, value in section_data.items():
            if name not in field_map:
                continue
            current = getattr(cfg, name)
            setattr(cfg, name, _coerce(value, current))

    # --- Step 2: overlay CLI values (only when explicitly provided) ---
    for name in field_map:
        if not hasattr(cli_namespace, name):
            continue
        val = getattr(cli_namespace, name)
        if val is None:
            continue
        current = getattr(cfg, name)
        setattr(cfg, name, _coerce(val, current))

    return cfg


def describe_config_section(cfg_class: type, section: str) -> str:
    """Render a human-readable summary of a config section's defaults."""
    if not is_dataclass(cfg_class):
        raise TypeError(f"{cfg_class!r} must be a dataclass")
    cfg = cfg_class()  # type: ignore[call-arg]
    lines = [f"[{section}]"]
    for f in fields(cfg):
        lines.append(f"  {f.name}: {getattr(cfg, f.name)!r}")
    return "\n".join(lines)
