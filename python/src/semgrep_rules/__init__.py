"""
Semgrep Python Rules Package.
"""

from importlib import resources
from pathlib import Path

__version__ = "0.1.1"


def _packaged_rules_path() -> Path:
    pkg_root = resources.files("semgrep_rules")
    return Path(str(pkg_root / "rules"))


def _dev_checkout_rules_path() -> Path:
    return Path(__file__).resolve().parent.parent.parent / "rules"


def get_rules_path() -> Path:
    packaged = _packaged_rules_path()
    if packaged.exists():
        return packaged

    dev_checkout = _dev_checkout_rules_path()
    if dev_checkout.exists():
        return dev_checkout

    raise FileNotFoundError(
        f"Python Semgrep rules not found at: {packaged} or {dev_checkout}"
    )
