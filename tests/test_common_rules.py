from dataclasses import dataclass
import json
from pathlib import Path
import subprocess
import sys
import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent
COMMON_QUALITY_DIR = REPO_ROOT / "common" / "rules" / "quality-tooling"
MAX_LINES_RULE = COMMON_QUALITY_DIR / "max-file-lines.yaml"
NO_COMPACTING_RULE = COMMON_QUALITY_DIR / "no-line-compacting.yaml"


@dataclass(frozen=True)
class FindingSummary:
    check_id: str
    severity: str


def run_semgrep_scan(config_path: Path, target_path: Path) -> tuple[FindingSummary, ...]:
    res = subprocess.run(
        ["semgrep", "scan", "--config", str(config_path), "--json", "--quiet", str(target_path)],
        capture_output=True,
        text=True,
        check=True,
    )
    findings = [
        FindingSummary(
            check_id=str(item["check_id"]),
            severity=str(item["extra"]["severity"]),
        )
        for item in json.loads(res.stdout)["results"]
    ]
    return tuple(findings)


def test_per_language_max_file_lines_duplicates_removed() -> None:
    assert not (REPO_ROOT / "python" / "rules" / "quality-tooling" / "max-file-lines.yaml").exists()
    assert not (REPO_ROOT / "csharp" / "rules" / "quality-tooling" / "max-file-lines.yaml").exists()
    assert not (REPO_ROOT / "bash" / "rules" / "quality-tooling" / "max-file-lines.yaml").exists()
    assert not (REPO_ROOT / "javascript" / "rules" / "quality-tooling" / "max-file-lines.yaml").exists()


def test_max_file_lines_is_warning_without_test_exemptions(tmp_path: Path) -> None:
    data = yaml.safe_load(MAX_LINES_RULE.read_text(encoding="utf-8"))
    rule = data["rules"][0]
    assert rule["id"] == "max-file-lines"
    assert rule["severity"] == "WARNING"
    assert "exclude" not in rule.get("paths", {})
    assert "Single-purpose components" in rule["message"]
    assert "compact" in rule["message"].lower()

    oversized_py_test = tmp_path / "tests" / "test_oversized.py"
    oversized_py_test.parent.mkdir(parents=True, exist_ok=True)
    oversized_py_test.write_text("assert True\n" * 201, encoding="utf-8")
    py_findings = run_semgrep_scan(MAX_LINES_RULE, oversized_py_test)
    assert len(py_findings) == 1
    assert py_findings[0].severity == "WARNING"

    oversized_cs_test = tmp_path / "OrderServiceTests.cs"
    oversized_cs_test.write_text("using System;\n" * 201, encoding="utf-8")
    cs_findings = run_semgrep_scan(MAX_LINES_RULE, oversized_cs_test)
    assert len(cs_findings) == 1

    compliant_file = tmp_path / "exact_200.py"
    compliant_file.write_text("x = 1\n" * 200, encoding="utf-8")
    assert run_semgrep_scan(MAX_LINES_RULE, compliant_file) == ()


def test_no_line_compacting_catches_horizontal_cramming_and_statement_packing(tmp_path: Path) -> None:
    data = yaml.safe_load(NO_COMPACTING_RULE.read_text(encoding="utf-8"))
    severities = {entry["id"]: entry["severity"] for entry in data["rules"]}
    assert severities == {
        "no-horizontal-line-cramming": "ERROR",
        "no-multi-statement-line-packing": "ERROR",
    }

    crammed = tmp_path / "crammed.py"
    crammed.write_text("result = " + " + ".join(["value_item"] * 22) + "\n", encoding="utf-8")
    crammed_ids = [item.check_id for item in run_semgrep_scan(NO_COMPACTING_RULE, crammed)]
    assert any(cid.endswith("no-horizontal-line-cramming") for cid in crammed_ids)

    packed = tmp_path / "packed.js"
    packed.write_text("const a = 1; const b = 2; const c = 3;\n", encoding="utf-8")
    packed_ids = [item.check_id for item in run_semgrep_scan(NO_COMPACTING_RULE, packed)]
    assert any(cid.endswith("no-multi-statement-line-packing") for cid in packed_ids)

    clean = tmp_path / "clean.js"
    clean.write_text(
        "const docs = 'https://thruput.se/agents/' + '" + ("a" * 200) + "';\n"
        "export const first = 1;\n"
        "export const second = 2;\n"
        "export const third = 3;\n"
        "for (let i = 0; i < 10; i++) {\n"
        "  console.log(i);\n"
        "}\n",
        encoding="utf-8",
    )
    assert run_semgrep_scan(NO_COMPACTING_RULE, clean) == ()


def test_language_clis_enforce_common_anti_compacting_rules(tmp_path: Path) -> None:
    packed_sh = tmp_path / "packed.sh"
    packed_sh.write_text("#!/usr/bin/env bash\nset -euo pipefail\na=1; b=2; c=3\n", encoding="utf-8")
    bash_res = subprocess.run(
        [str(REPO_ROOT / "bash" / "bin" / "semgrep-bash"), "--json", "--quiet", str(packed_sh)],
        capture_output=True,
        text=True,
        check=False,
    )
    bash_ids = [r["check_id"] for r in json.loads(bash_res.stdout)["results"]]
    assert any(cid.endswith("no-multi-statement-line-packing") for cid in bash_ids)

    packed_py = tmp_path / "packed.py"
    packed_py.write_text("a = 1; b = 2; c = 3\n", encoding="utf-8")
    py_env = {"PYTHONPATH": str(REPO_ROOT / "python" / "src"), "PATH": subprocess.os.environ["PATH"]}
    py_res = subprocess.run(
        [sys.executable, "-m", "semgrep_rules.cli", "--json", "--quiet", str(packed_py)],
        capture_output=True,
        text=True,
        env=py_env,
        check=False,
    )
    py_ids = [r["check_id"] for r in json.loads(py_res.stdout)["results"]]
    assert any(cid.endswith("no-multi-statement-line-packing") for cid in py_ids)
