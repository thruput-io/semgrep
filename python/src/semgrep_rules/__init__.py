"""
Semgrep Python Rules Package.
"""

from importlib import resources
from pathlib import Path
from typing import Literal

__version__ = "0.1.1"

SupportedLanguage = Literal["python", "bash", "csharp"]


def _packaged_rules_path(lang: SupportedLanguage) -> Path:
    pkg_root = resources.files("semgrep_rules")
    return Path(str(pkg_root / lang / "rules"))


def _dev_checkout_rules_path(lang: SupportedLanguage) -> Path:
    return Path(__file__).resolve().parent.parent.parent.parent / lang / "rules"


def get_rules_path(lang: SupportedLanguage = "python") -> Path:
    """
    Returns the absolute Path to the Semgrep rules directory for the given language.
    """
    packaged = _packaged_rules_path(lang)
    if packaged.exists():
        return packaged

    dev_checkout = _dev_checkout_rules_path(lang)
    if dev_checkout.exists():
        return dev_checkout

    raise FileNotFoundError(
        f"Semgrep rules for language '{lang}' not found at: {packaged} or {dev_checkout}"
    )
