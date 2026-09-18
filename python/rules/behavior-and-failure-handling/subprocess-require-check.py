import subprocess

def run_commands():
    # ruleid: python-subprocess-require-check
    subprocess.run(["pytest", "tests/"])

    # ok: python-subprocess-require-check
    subprocess.run(["pytest", "tests/"], check=True)

    # ok: python-subprocess-require-check
    res = subprocess.run(["pytest", "tests/"])
    if res.returncode != 0:
        raise RuntimeError("failed")
