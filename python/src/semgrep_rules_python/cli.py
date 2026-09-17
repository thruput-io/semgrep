"""
CLI runner for semgrep-python.
"""

import argparse
import subprocess
import sys
from . import get_rules_path, __version__


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        prog="semgrep-python",
        description="Run packaged Python Semgrep rules against your codebase.",
        add_help=False
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}"
    )

    _, remaining_args = parser.parse_known_args(argv)

    try:
        rules_path = str(get_rules_path())
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    cmd = ["semgrep", "--config", rules_path] + remaining_args

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


if __name__ == "__main__":
    sys.exit(main())
