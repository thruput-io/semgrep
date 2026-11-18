from pathlib import Path
from scripts.sync_audit import audit_repository

REPO_ROOT = Path(__file__).resolve().parent.parent


def write_sample_upstream(upstream_dir: Path) -> None:
    (upstream_dir / "Rules.yaml").write_text(
        "rules:\n"
        "- id: Single-purpose components\n"
        "  marker: MUST\n"
        "  group: Domain Model\n"
        "  parent: Separation of Concerns\n"
        "  body: |\n"
        "    Decompose code into small, single-purpose [[Component]]s.\n"
        "  smells:\n"
        "  - A [[Component]] longer than 200 lines.\n"
        "- id: No silent catch\n"
        "  marker: MUST NOT\n"
        "  group: Failure Handling\n"
        "  parent: Fail fast\n"
        "  body: |\n"
        "    Use [[Try/catch block]]s that do not [[Rethrow]].\n",
        encoding="utf-8",
    )
    (upstream_dir / "Principles.yaml").write_text(
        "principles:\n"
        "- id: Separation of Concerns\n"
        "  parent: One concern, one owner\n"
        "  body: |\n"
        "    Each concern has one owner in one layer.\n"
        "- id: Fail fast\n"
        "  parent: Crash, don't guess\n"
        "  body: |\n"
        "    A system fails loudly and at once.\n",
        encoding="utf-8",
    )
    (upstream_dir / "Rationales.yaml").write_text(
        "rationales:\n"
        "- id: One concern, one owner\n"
        "  parent: Easy to Change\n"
        "  body: |\n"
        "    Hide each design decision behind one interface.\n"
        "  solutions:\n"
        "  - marker: SHOULD\n"
        "    body: |\n"
        "      Hide each design decision likely to change behind one module interface.\n"
        "- id: Crash, don't guess\n"
        "  parent: Shift Left\n"
        "  body: |\n"
        "    Stop at once on unexpected state.\n"
        "  solutions:\n"
        "  - marker: SHOULD\n"
        "    body: |\n"
        "      Leave recovery to a supervisor outside the failing process.\n",
        encoding="utf-8",
    )


def write_sample_repo(repo_dir: Path) -> None:
    docs_dir = repo_dir / "docs"
    docs_dir.mkdir(parents=True)
    (docs_dir / "rule-detection-matrix.md").write_text(
        "| Rule | Semgrep | Arch-Test | AI-Reasoning | Rationale |\n"
        "| :--- | :---: | :---: | :---: | :--- |\n"
        "| `Single-purpose components` | **9** | 8 | 6 | Common rule |\n"
        "| `File too large` | **10** | 4 | 1 | Retired rule |\n",
        encoding="utf-8",
    )

    common_dir = repo_dir / "common" / "rules" / "quality-tooling"
    common_dir.mkdir(parents=True)
    (common_dir / "max-file-lines.yaml").write_text(
        "rules:\n"
        "  - id: max-file-lines\n"
        "    message: Warn\n"
        "    severity: ERROR\n"
        "    languages: [generic]\n"
        "    pattern: x\n"
        "    metadata:\n"
        "      category: quality-tooling\n"
        "      rule: Single-purpose components\n"
        "      smell: A [[Component]] longer than 200 lines.\n",
        encoding="utf-8",
    )

    py_dir = repo_dir / "python" / "rules" / "domain-modeling"
    py_dir.mkdir(parents=True)
    (py_dir / "no-unwrapping.yaml").write_text(
        "rules:\n"
        "  - id: python-no-unwrapping\n"
        "    message: Retired\n"
        "    severity: ERROR\n"
        "    languages: [python]\n"
        "    pattern: x\n"
        "    metadata:\n"
        "      category: domain-modeling\n"
        "      rule: No unwrapping\n"
        "  - id: python-unmapped\n"
        "    message: Unmapped\n"
        "    severity: ERROR\n"
        "    languages: [python]\n"
        "    pattern: y\n"
        "    metadata:\n"
        "      category: domain-modeling\n",
        encoding="utf-8",
    )


def test_sync_audit_detects_matrix_deltas_orphans_severity_and_solution_chains(tmp_path: Path) -> None:
    upstream_dir = tmp_path / "upstream"
    upstream_dir.mkdir()
    repo_dir = tmp_path / "repo"
    repo_dir.mkdir()
    write_sample_upstream(upstream_dir)
    write_sample_repo(repo_dir)

    report = audit_repository(upstream_dir, repo_dir)
    assert report.removed_from_matrix == ("File too large",)
    assert report.missing_from_matrix == ("No silent catch",)
    assert report.orphaned_semgrep_rules == (
        "python/rules/domain-modeling/no-unwrapping.yaml::python-no-unwrapping::No unwrapping",
    )
    assert report.unmapped_semgrep_rules == (
        "python/rules/domain-modeling/no-unwrapping.yaml::python-unmapped",
    )
    assert report.smell_severity_mismatches == (
        "common/rules/quality-tooling/max-file-lines.yaml::max-file-lines::ERROR",
    )

    chain = report.chain_for("Single-purpose components")
    assert chain.principle_id == "Separation of Concerns"
    assert chain.rationale_id == "One concern, one owner"
    assert chain.published_url == "https://thruput.se/agents/#single-purpose-components"
    assert chain.ancestor_solutions == (
        "SHOULD: Hide each design decision likely to change behind one module interface.",
    )
