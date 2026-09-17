"""
Semgrep Python Rules Package.
"""

from importlib import resources
from pathlib import Path

__version__ = "0.1.0"


def get_rules_path() -> Path:
    """
    Returns the absolute Path to the Python Semgrep rules directory.
    """
    # 1. Check if bundled in package data
    try:
        pkg_root = resources.files("semgrep_rules")
        pkg_rules = Path(str(pkg_root / "rules"))
        if pkg_rules.exists():
            return pkg_rules
    except Exception:
        pass

    # 2. Check python/rules directory (development & local installs)
    repo_rules = Path(__file__).resolve().parent.parent.parent / "rules"
    if repo_rules.exists():
        return repo_rules

    raise FileNotFoundError(f"Python Semgrep rules not found at: {repo_rules}")
