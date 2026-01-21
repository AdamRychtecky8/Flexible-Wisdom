"""Lightweight config helpers for local, private data access.

- Reads DATA_DIR from environment (optionally from a local .env).
- Verifies the path exists without touching contents.
- Provides stable project sub-paths for outputs and reports.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


def load_env(env_path: Optional[Path | str] = None) -> None:
    """Populate os.environ from a .env file if present (no external deps).

    Only fills missing keys; existing environment variables win.
    """
    path = Path(env_path) if env_path else Path(".env")
    if not path.exists():
        return

    for line in path.read_text().splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if "=" not in stripped:
            continue

        key, value = stripped.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and value and key not in os.environ:
            os.environ[key] = value


@dataclass(frozen=True)
class ProjectPaths:
    data_dir: Path
    outputs_dir: Path
    reports_dir: Path


def get_paths(env_path: Optional[Path | str] = None) -> ProjectPaths:
    """Return validated project paths based on DATA_DIR.

    Raises if DATA_DIR is unset or missing so failures are early and clear.
    """
    load_env(env_path)

    data_dir = os.environ.get("DATA_DIR")
    if not data_dir:
        raise RuntimeError("DATA_DIR not set. Copy .env.example to .env and set your OneDrive path.")

    data_path = Path(data_dir).expanduser().resolve()
    if not data_path.exists():
        raise FileNotFoundError(
            f"DATA_DIR does not exist: {data_path}. Create a junction/symlink to your OneDrive data."
        )

    project_root = Path(__file__).resolve().parent.parent
    outputs_dir = project_root / "outputs"
    reports_dir = project_root / "reports"
    outputs_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)

    return ProjectPaths(data_dir=data_path, outputs_dir=outputs_dir, reports_dir=reports_dir)


__all__ = ["get_paths", "load_env", "ProjectPaths"]
