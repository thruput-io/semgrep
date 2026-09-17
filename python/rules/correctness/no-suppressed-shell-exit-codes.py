import subprocess

def run_commands():
    # ruleid: python-no-suppressed-shell-exit-codes
    cmd1 = "npm test || true"

    # ruleid: python-no-suppressed-shell-exit-codes
    cmd2 = "ls -la 2>/dev/null"

    # ruleid: python-no-suppressed-shell-exit-codes
    cmd3 = "cat log.txt > /dev/null 2>&1"

    # ok: python-no-suppressed-shell-exit-codes
    safe_cmd = "npm test && pytest"
