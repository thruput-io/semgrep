import glob
import os
import shutil
import subprocess
import yaml
import pytest
from semgrep_rules_python import get_rules_path

RULES_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src", "semgrep_rules_python", "rules"))

def find_rule_files():
    """Find all yaml rule files under python rules directory."""
    pattern = os.path.join(RULES_ROOT, "**", "*.yaml")
    return sorted(glob.glob(pattern, recursive=True))

PYTHON_RULE_FILES = find_rule_files()

def get_rule_id(rule_file_path):
    rel_path = os.path.relpath(rule_file_path, RULES_ROOT)
    return rel_path.replace(os.sep, "::")


def get_semgrep_executable():
    """Locate semgrep binary or fail the test suite immediately (fail-closed)."""
    semgrep_bin = shutil.which("semgrep")
    if not semgrep_bin:
        pytest.fail(
            "CRITICAL: 'semgrep' binary was not found in PATH. "
            "Install Semgrep via: pip install semgrep"
        )
    return semgrep_bin


class TestPythonPackageIntegrity:

    def test_get_rules_path(self):
        """Verify that get_rules_path() returns an existing path containing Python rules."""
        path = get_rules_path()
        assert path.exists(), f"Path does not exist: {path}"
        assert len(list(path.glob("**/*.yaml"))) > 0, "No Python yaml rules found in package path"


class TestPythonRulesIntegrity:

    def test_rules_directory_is_not_empty(self):
        """Ensure Python rules exist."""
        assert len(PYTHON_RULE_FILES) > 0, "No Python rule YAML files found"

    def test_semgrep_cli_validates_python_rules(self):
        """Runs `semgrep --validate --config rules/` across Python rules."""
        semgrep_bin = get_semgrep_executable()
        result = subprocess.run(
            [semgrep_bin, "--validate", "--config", RULES_ROOT],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, (
            f"Global Semgrep Python rule validation failed!\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )

    @pytest.mark.parametrize("rule_file", PYTHON_RULE_FILES, ids=get_rule_id)
    def test_yaml_syntax_and_structure(self, rule_file):
        """Verify that every YAML file is syntactically valid YAML."""
        with open(rule_file, "r", encoding="utf-8") as f:
            try:
                data = yaml.safe_load(f)
            except yaml.YAMLError as exc:
                pytest.fail(f"YAML parsing error in {rule_file}: {exc}")

        assert isinstance(data, dict), f"{rule_file} must contain a top-level mapping"
        assert "rules" in data, f"{rule_file} missing top-level 'rules' key"
        assert isinstance(data["rules"], list), f"{rule_file} 'rules' key must be a list"
        assert len(data["rules"]) > 0, f"{rule_file} must contain at least one rule"

    @pytest.mark.parametrize("rule_file", PYTHON_RULE_FILES, ids=get_rule_id)
    def test_rule_metadata_and_schema(self, rule_file):
        """Verify required fields, severity levels, languages, and metadata."""
        with open(rule_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        valid_severities = {"INFO", "WARNING", "ERROR"}

        for rule in data["rules"]:
            rule_id = rule.get("id")
            assert rule_id, f"Rule in {rule_file} missing 'id'"
            assert rule_id.startswith("python-"), f"Rule ID '{rule_id}' should start with 'python-'"
            assert "message" in rule and len(rule["message"].strip()) > 0, f"Rule {rule_id} missing message"
            assert "languages" in rule and "python" in rule["languages"], f"Rule {rule_id} missing 'python' language"
            assert "severity" in rule and rule["severity"] in valid_severities, (
                f"Rule {rule_id} has invalid severity '{rule.get('severity')}'"
            )
            assert "metadata" in rule and isinstance(rule["metadata"], dict), f"Rule {rule_id} missing 'metadata'"
            assert "category" in rule["metadata"], f"Rule {rule_id} missing 'category' under metadata"

    @pytest.mark.parametrize("rule_file", PYTHON_RULE_FILES, ids=get_rule_id)
    def test_rule_has_matching_test_fixture(self, rule_file):
        """Verify that every Python rule has a corresponding .py test fixture."""
        base, _ = os.path.splitext(rule_file)
        py_fixture = f"{base}.py"
        assert os.path.exists(py_fixture), f"Missing test fixture for {rule_file}. Expected '{base}.py'"

    @pytest.mark.parametrize("rule_file", PYTHON_RULE_FILES, ids=get_rule_id)
    def test_test_fixture_contains_ruleid_and_ok_annotations(self, rule_file):
        """Ensure test fixtures have both positive (ruleid) and negative (ok) test cases."""
        with open(rule_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)

        base, _ = os.path.splitext(rule_file)
        fixture_path = f"{base}.py"

        with open(fixture_path, "r", encoding="utf-8") as f:
            fixture_content = f.read()

        for rule in data["rules"]:
            rule_id = rule["id"]
            has_positive_test = f"ruleid: {rule_id}" in fixture_content or f"ruleid:{rule_id}" in fixture_content
            has_negative_test = f"ok: {rule_id}" in fixture_content or f"ok:{rule_id}" in fixture_content

            assert has_positive_test, f"Fixture {fixture_path} missing '# ruleid: {rule_id}'"
            assert has_negative_test, f"Fixture {fixture_path} missing '# ok: {rule_id}'"

    @pytest.mark.parametrize("rule_file", PYTHON_RULE_FILES, ids=get_rule_id)
    def test_semgrep_test_execution(self, rule_file):
        """Execute `semgrep --test <rule_file>` against Python fixture."""
        semgrep_bin = get_semgrep_executable()
        result = subprocess.run(
            [semgrep_bin, "--test", rule_file],
            capture_output=True,
            text=True
        )
        assert result.returncode == 0, (
            f"Semgrep test execution failed for {rule_file}!\n"
            f"STDOUT:\n{result.stdout}\n"
            f"STDERR:\n{result.stderr}"
        )
