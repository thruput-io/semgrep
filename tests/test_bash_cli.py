import json
import os
import shutil
import subprocess

import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT_PATH = os.path.join(REPO_ROOT, "bash", "bin", "semgrep-bash")
BASH_RULES_ROOT = os.path.join(REPO_ROOT, "bash", "rules")
BAD_FIXTURE = os.path.join(BASH_RULES_ROOT, "purpose-and-accuracy", "require-shebang.sh")
OK_FIXTURE = os.path.join(BASH_RULES_ROOT, "purpose-and-accuracy", "require-shebang.ok.sh")


def require_semgrep():
    semgrep_bin = shutil.which("semgrep")
    if not semgrep_bin:
        pytest.fail(
            "CRITICAL: 'semgrep' executable was not found in PATH. "
            "Install Semgrep via: pip install semgrep"
        )
    return semgrep_bin


def run_script(args, env=None):
    return subprocess.run(
        [SCRIPT_PATH] + args,
        capture_output=True,
        text=True,
        env=env,
    )


class TestSemgrepBashScript:

    def test_script_exists_and_is_executable(self):
        assert os.path.isfile(SCRIPT_PATH), f"Missing standalone script at {SCRIPT_PATH}"
        assert os.access(SCRIPT_PATH, os.X_OK), f"{SCRIPT_PATH} must be executable"

    def test_detects_violation_in_known_bad_fixture(self):
        require_semgrep()
        result = run_script(["--json", "--quiet", BAD_FIXTURE])
        payload = json.loads(result.stdout)
        check_ids = [r["check_id"] for r in payload["results"]]
        assert any(cid.endswith("require-shebang") for cid in check_ids), (
            f"Expected 'require-shebang' finding, got: {check_ids}"
        )

    def test_silent_on_compliant_fixture(self):
        require_semgrep()
        result = run_script(["--json", "--quiet", OK_FIXTURE])
        payload = json.loads(result.stdout)
        assert payload["results"] == [], f"Unexpected findings: {payload['results']}"

    def test_defaults_target_to_current_directory_when_no_positional_args(self, tmp_path):
        require_semgrep()
        result = run_script(["--json", "--quiet"])
        assert result.returncode in (0, 1), (
            f"Unexpected crash with no positional args.\nSTDOUT:{result.stdout}\nSTDERR:{result.stderr}"
        )
        json.loads(result.stdout)

    def test_errors_clearly_when_semgrep_not_on_path(self):
        semgrep_bin = require_semgrep()
        semgrep_dir = os.path.dirname(semgrep_bin)
        remaining_dirs = [d for d in os.environ.get("PATH", "").split(os.pathsep) if d != semgrep_dir]
        stripped_env = {**os.environ, "PATH": os.pathsep.join(remaining_dirs)}
        result = run_script([BAD_FIXTURE], env=stripped_env)
        assert result.returncode == 1
        assert "semgrep" in result.stderr.lower()
