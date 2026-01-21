# notebooks/_utils.py — Utilities for notebooks
#
# NOTE: For data loading, prefer importing from src.data_loaders:
#   from src.data_loaders import load_human_master, load_model_master, load_bio_master
#
# This file contains legacy helpers; keep for backward compatibility.

from pathlib import Path
import os
import sys

def get_data_dir() -> Path:
    """Legacy helper: get DATA_DIR from environment.
    
    DEPRECATED: Use src.config.get_paths() instead.
    Kept for backward compatibility with older notebooks.
    """
    # Try to load from .env first
    env_path = Path.cwd() / ".env"
    if env_path.exists():
        for line in env_path.read_text().splitlines():
            stripped = line.strip()
            if stripped.startswith("DATA_DIR="):
                data_dir = stripped.split("=", 1)[1].strip()
                return Path(data_dir).expanduser().resolve()
    
    # Fall back to os.getenv
    data_dir = os.getenv("DATA_DIR")
    if not data_dir or not Path(data_dir).exists():
        raise FileNotFoundError(
            "DATA_DIR is not set or path does not exist. "
            "Create a .env file (see .env.example) and set DATA_DIR to your data path."
        )
    return Path(data_dir)


# For new notebooks, use: from src.data_loaders import load_human_master, etc.
__all__ = ["get_data_dir"]
