import subprocess
import os

def run_failing_command():
    # ruleid: python-no-subprocess-discard-stderr
    subprocess.run(["git", "status"], stderr=subprocess.DEVNULL)

    # ruleid: python-no-subprocess-discard-stderr
    subprocess.Popen(["ls", "-la"], stderr=os.devnull)

def run_safe_command():
    # ok: python-no-subprocess-discard-stderr
    subprocess.run(["git", "status"], check=True)

    # ok: python-no-subprocess-discard-stderr
    subprocess.Popen(["ls", "-la"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
