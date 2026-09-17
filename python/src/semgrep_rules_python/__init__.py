"""
Semgrep Python Rules Package.
"""

from importlib import resources
from pathlib import Path

__version__ = "0.1.0"


def get_rules_path() -> Path:
    """
    Returns the absolute Path to the packaged Python Semgrep rules directory.
    """
    pkg_root = resources.files("semgrep_rules_python")
    pkg_rules = Path(str(pkg_root / "rules"))

    if pkg_rules.exists():
        return pkg_rules

    # Fallback to source directory during local development
    fallback = Path(__file__).resolve().parent / "rules"
    if fallback.exists():
        return fallback

    raise FileNotFoundError(f"Python Semgrep rules not found in package at: {pkg_rules}")
