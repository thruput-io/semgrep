import subprocess

def run_user_command(user_filename):
    # ruleid: python-subprocess-shell-true
    subprocess.Popen(f"ls -la {user_filename}", shell=True)

    # ruleid: python-subprocess-shell-true
    subprocess.run("cat " + user_filename, shell=True)

    # ok: python-subprocess-shell-true
    subprocess.run(["ls", "-la", user_filename])

    # ok: python-subprocess-shell-true
    subprocess.run("ls -la", shell=True)
