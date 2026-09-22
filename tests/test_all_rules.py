import glob
import json
import os
import shutil
import subprocess
import yaml
import pytest

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PYTHON_RULES_ROOT = os.path.join(REPO_ROOT, "python", "rules")
CSHARP_RULES_ROOT = os.path.join(REPO_ROOT, "csharp", "rules")
BASH_RULES_ROOT = os.path.join(REPO_ROOT, "bash", "rules")

def get_all_rule_files():
    """Discover all YAML rule files across Python, C#, and Bash directories."""
    python_rules = sorted(glob.glob(os.path.join(PYTHON_RULES_ROOT, "**", "*.yaml"), recursive=True))
    csharp_rules = sorted(glob.glob(os.path.join(CSHARP_RULES_ROOT, "**", "*.yaml"), recursive=True))
    bash_rules = sorted(glob.glob(os.path.join(BASH_RULES_ROOT, "**", "*.yaml"), recursive=True))
    return python_rules + csharp_rules + bash_rules

ALL_RULE_FILES = get_all_rule_files()

def get_rule_test_id(rule_path):
    """Format readable test ID e.g. python::correctness::mutable-default-arg."""
    rel = os.path.relpath(rule_path, REPO_ROOT)
    return rel.replace(os.sep, "::").replace("rules::", "")


def resolve_fixture_files(base):
    """
    Resolve the positive and negative fixture files for a rule.

    Most rules use one fixture file carrying both '# ruleid:' and '# ok:'
    lines. A whole-file-scope rule (e.g. "file must start with a shebang")
    cannot hold both cases at once, since the property being checked is a
    single fact about the whole file. Such rules provide a second file,
    '<base>.ok.<ext>', carrying only the negative case; if present, it is
    used for the negative test instead of the primary fixture file.
    """
    for ext in (".py", ".cs", ".sh", ".bats"):
        primary = f"{base}{ext}"
        if os.path.exists(primary):
            ok_variant = f"{base}.ok{ext}"
            negative = ok_variant if os.path.exists(ok_variant) else primary
            return primary, negative
    raise FileNotFoundError(
        f"No test fixture found for rule base '{base}' (checked .py, .cs, .sh, .bats)"
    )


def get_semgrep_bin():
    """Locate semgrep binary or fail the test suite immediately (fail-closed)."""
    semgrep_bin = shutil.which("semgrep")
    if not semgrep_bin:
        pytest.fail(
            "CRITICAL: 'semgrep' executable was not found in PATH. "
            "Install Semgrep via: pip install semgrep"
        )
    return semgrep_bin


def run_semgrep_json_scan(rule_file, fixture_file):
    """Execute Semgrep on the fixture file with the given rule and return JSON output."""
    semgrep_bin = get_semgrep_bin()
    res = subprocess.run(
        [
            semgrep_bin,
            "scan",
            "--config", rule_file,
            "--json",
            "--quiet",
            fixture_file
        ],
        capture_output=True,
        text=True
    )
    try:
        return json.loads(res.stdout)
    except json.JSONDecodeError:
        pytest.fail(
            f"Failed to parse Semgrep JSON output for {rule_file}!\n"
            f"STDOUT:\n{res.stdout}\nSTDERR:\n{res.stderr}"
        )


def matches_for_rule(results, rule_id):
    return [r for r in results if r.get("check_id") == rule_id or r.get("check_id", "").endswith(f".{rule_id}")]


def assert_rule_triggers_near(rule_matches, rule_id, fixture_file, expected_lines):
    assert len(rule_matches) > 0, (
        f"POSITIVE TEST FAILED: Rule '{rule_id}' produced 0 findings in {fixture_file}.\n"
        f"Expected detections on lines following: {expected_lines}"
    )
    matched_lines = [r["start"]["line"] for r in rule_matches]
    for expected_line in expected_lines:
        found_near = any(expected_line <= m_line <= expected_line + 3 for m_line in matched_lines)
        assert found_near, (
            f"POSITIVE TEST FAILED: Rule '{rule_id}' was expected to trigger near comment line {expected_line}, "
            f"but actual findings were on lines: {matched_lines}"
        )


def assert_rule_silent_near(rule_matches, rule_id, fixture_file, guarded_lines):
    matched_lines = [r["start"]["line"] for r in rule_matches]
    for guarded_line in guarded_lines:
        false_positive_found = any(guarded_line <= m_line <= guarded_line + 3 for m_line in matched_lines)
        assert not false_positive_found, (
            f"NEGATIVE TEST FAILED (FALSE POSITIVE): Rule '{rule_id}' incorrectly triggered on safe code "
            f"near line {guarded_line} in {fixture_file}!"
        )


def parse_fixture_annotation_lines(fixture_path, rule_id):
    """Find line numbers for positive (# ruleid:) and negative (# ok:) comments in fixture."""
    with open(fixture_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    positive_comment_lines = []
    negative_comment_lines = []

    for idx, line in enumerate(lines, start=1):
        if f"ruleid: {rule_id}" in line or f"ruleid:{rule_id}" in line:
            positive_comment_lines.append(idx)
        elif f"ok: {rule_id}" in line or f"ok:{rule_id}" in line:
            negative_comment_lines.append(idx)

    return positive_comment_lines, negative_comment_lines


class TestPerRulePositiveAndNegativeCases:
    """
    Explicit Positive and Negative unit tests for every individual rule in the project.
    """

    @pytest.mark.parametrize("rule_file", ALL_RULE_FILES, ids=get_rule_test_id)
    def test_positive_case_triggers_finding(self, rule_file):
        with open(rule_file, "r", encoding="utf-8") as f:
            rule_data = yaml.safe_load(f)

        base, _ = os.path.splitext(rule_file)
        fixture_file, _ = resolve_fixture_files(base)

        scan_output = run_semgrep_json_scan(rule_file, fixture_file)
        results = scan_output.get("results", [])

        for rule in rule_data["rules"]:
            rule_id = rule["id"]
            pos_lines, _ = parse_fixture_annotation_lines(fixture_file, rule_id)
            assert len(pos_lines) > 0, f"Fixture {fixture_file} has no positive test annotations for '{rule_id}'"
            assert_rule_triggers_near(matches_for_rule(results, rule_id), rule_id, fixture_file, pos_lines)

    @pytest.mark.parametrize("rule_file", ALL_RULE_FILES, ids=get_rule_test_id)
    def test_negative_case_zero_false_positives(self, rule_file):
        with open(rule_file, "r", encoding="utf-8") as f:
            rule_data = yaml.safe_load(f)

        base, _ = os.path.splitext(rule_file)
        _, fixture_file = resolve_fixture_files(base)

        scan_output = run_semgrep_json_scan(rule_file, fixture_file)
        results = scan_output.get("results", [])

        for rule in rule_data["rules"]:
            rule_id = rule["id"]
            _, neg_lines = parse_fixture_annotation_lines(fixture_file, rule_id)
            assert len(neg_lines) > 0, f"Fixture {fixture_file} has no negative guard annotations for '{rule_id}'"
            assert_rule_silent_near(matches_for_rule(results, rule_id), rule_id, fixture_file, neg_lines)


class TestRulesStructureAndSchema:
    """
    Schema, YAML validity, and metadata tests.
    """

    @pytest.mark.parametrize("rule_file", ALL_RULE_FILES, ids=get_rule_test_id)
    def test_yaml_syntax_and_schema(self, rule_file):
        with open(rule_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        assert isinstance(data, dict) and "rules" in data and len(data["rules"]) > 0

    @pytest.mark.parametrize("rule_file", ALL_RULE_FILES, ids=get_rule_test_id)
    def test_rule_metadata_conventions(self, rule_file):
        with open(rule_file, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        for rule in data["rules"]:
            assert rule.get("id")
            assert rule.get("message")
            assert rule.get("languages")
            assert rule.get("severity") in {"INFO", "WARNING", "ERROR"}
            assert "category" in rule.get("metadata", {})
