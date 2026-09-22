"""
CLI runner for semgrep-python.
"""

import argparse
import subprocess
import sys
from typing import Optional, Sequence

from . import SupportedLanguage, get_rules_path, __version__


def main(argv: Optional[Sequence[str]] = None, lang: SupportedLanguage = "python") -> int:
    parser = argparse.ArgumentParser(
        prog=f"semgrep-{lang}",
        description=f"Run {lang.title()} Semgrep rules against your codebase.",
        add_help=False
    )
    parser.add_argument(
        "--lang",
        choices=["python", "bash", "csharp"],
        default=lang,
        help="Language ruleset to run"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    args, remaining_args = parser.parse_known_args(argv)

    target_lang: SupportedLanguage = args.lang
    try:
        rules_path = str(get_rules_path(target_lang))
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    cmd = ["semgrep", "--error", "--config", rules_path] + list(remaining_args)

    if not any(not arg.startswith("-") for arg in remaining_args):
        cmd.append(".")

    try:
        result = subprocess.run(cmd)
        return result.returncode
    except FileNotFoundError:
        print(
            "Error: 'semgrep' executable was not found. Please install semgrep via: pip install semgrep",
            file=sys.stderr
        )
        return 1


def bash_main(argv: Optional[Sequence[str]] = None) -> int:
    return main(argv, lang="bash")


if __name__ == "__main__":
    sys.exit(main())
