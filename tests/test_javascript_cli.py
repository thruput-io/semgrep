import json
import os
import shutil
import subprocess

import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
SCRIPT_PATH = os.path.join(REPO_ROOT, "javascript", "bin", "semgrep-javascript")
JS_RULES_ROOT = os.path.join(REPO_ROOT, "javascript", "rules")
OK_FIXTURE = os.path.join(JS_RULES_ROOT, "quality-tooling", "max-file-lines.ok.js")


def require_semgrep():
    semgrep_bin = shutil.which("semgrep")
    assert semgrep_bin is not None, (
        "CRITICAL: 'semgrep' executable was not found in PATH. "
        "Install Semgrep via: pip install semgrep"
    )
    return semgrep_bin


def run_script(args):
    return subprocess.run(
        [SCRIPT_PATH] + args,
        capture_output=True,
        text=True,
    )


def run_script_with_env(args, env):
    return subprocess.run(
        [SCRIPT_PATH] + args,
        capture_output=True,
        text=True,
        env=env,
    )


class TestSemgrepJavascriptScript:

    def test_script_exists_and_is_executable(self):
        assert os.path.isfile(SCRIPT_PATH), f"Missing standalone script at {SCRIPT_PATH}"
        assert os.access(SCRIPT_PATH, os.X_OK), f"{SCRIPT_PATH} must be executable"

    def test_detects_violation_in_known_bad_fixture(self, tmp_path):
        require_semgrep()
        bad_fixture = tmp_path / "max-file-lines.js"
        bad_fixture.write_text("export const x = 1;\n" * 201, encoding="utf-8")
        result = run_script(["--json", "--quiet", str(bad_fixture)])
        payload = json.loads(result.stdout)
        assert len(payload["results"]) == 1
        assert payload["results"][0]["check_id"].endswith("max-file-lines")

    def test_silent_on_compliant_fixture(self):
        require_semgrep()
        result = run_script(["--json", "--quiet", OK_FIXTURE])
        payload = json.loads(result.stdout)
        assert payload["results"] == [], f"Unexpected findings: {payload['results']}"

    def test_defaults_target_to_current_directory_when_no_positional_args(self, tmp_path, monkeypatch):
        require_semgrep()
        (tmp_path / "clean.js").write_text("export const x = 1;\n", encoding="utf-8")
        monkeypatch.chdir(tmp_path)
        result = run_script(["--json", "--quiet"])
        payload = json.loads(result.stdout)
        assert result.returncode == 0
        assert payload["results"] == []

    def test_errors_clearly_when_semgrep_not_on_path(self):
        stripped_env = {**os.environ, "PATH": "/usr/bin:/bin"}
        result = run_script_with_env([OK_FIXTURE], stripped_env)
        assert result.returncode == 1
        assert "semgrep" in result.stderr.lower()
