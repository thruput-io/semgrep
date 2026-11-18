"""
CLI runner for semgrep-python.
"""

import argparse
import subprocess
import sys
from typing import Sequence

from . import get_rule_paths, __version__


def run_cli(argv: Sequence[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="semgrep-python",
        description="Run Python Semgrep rules against your codebase.",
        add_help=False,
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )

    _, remaining_args = parser.parse_known_args(argv)

    try:
        rule_paths = get_rule_paths()
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    cmd = ["semgrep", "--error"]
    for path in rule_paths:
        cmd.extend(["--config", str(path)])
    cmd.extend(remaining_args)

    if not any(not arg.startswith("-") for arg in remaining_args):
        cmd.append(".")

    try:
        result = subprocess.run(cmd)
        return result.returncode
    except FileNotFoundError:
        print(
            "Error: 'semgrep' executable was not found. Please install semgrep via: pip install semgrep",
            file=sys.stderr,
        )
        return 1


def main() -> int:
    return run_cli(sys.argv[1:])


if __name__ == "__main__":
    sys.exit(main())
