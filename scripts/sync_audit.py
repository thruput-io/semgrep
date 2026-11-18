from dataclasses import asdict, dataclass
import json
from pathlib import Path
import re
import sys
import yaml

RULE_DIRS: tuple[str, ...] = ("common", "python", "csharp", "bash", "bats", "javascript")


@dataclass(frozen=True)
class RuleChain:
    rule_id: str
    marker: str
    group: str
    principle_id: str
    rationale_id: str
    published_url: str
    smells: tuple[str, ...]
    ancestor_solutions: tuple[str, ...]


@dataclass(frozen=True)
class SyncAuditReport:
    removed_from_matrix: tuple[str, ...]
    missing_from_matrix: tuple[str, ...]
    orphaned_semgrep_rules: tuple[str, ...]
    unmapped_semgrep_rules: tuple[str, ...]
    smell_severity_mismatches: tuple[str, ...]
    rule_chains: tuple[RuleChain, ...]

    def chain_for(self, rule_id: str) -> RuleChain:
        for chain in self.rule_chains:
            if chain.rule_id == rule_id:
                return chain
        raise KeyError(f"Unknown rule_id: {rule_id}")


def slugify_id(entry_id: str) -> str:
    lowered = entry_id.strip().lower()
    cleaned = re.sub(r"[^a-z0-9\s-]", "", lowered)
    return re.sub(r"[\s-]+", "-", cleaned).strip("-")


def format_solutions(raw_items: list) -> list[str]:
    formatted = []
    for item in raw_items:
        body = " ".join(str(item["body"]).strip().split())
        formatted.append(f"{item['marker']}: {body}")
    return formatted


def load_rule_chains(upstream_dir: Path) -> tuple[RuleChain, ...]:
    rules_data = yaml.safe_load((upstream_dir / "Rules.yaml").read_text(encoding="utf-8"))["rules"]
    principles_by_id = {
        item["id"]: item
        for item in yaml.safe_load((upstream_dir / "Principles.yaml").read_text(encoding="utf-8"))["principles"]
    }
    rationales_by_id = {
        item["id"]: item
        for item in yaml.safe_load((upstream_dir / "Rationales.yaml").read_text(encoding="utf-8"))["rationales"]
    }

    chains = []
    for rule in rules_data:
        rule_id = str(rule["id"])
        principle_id = str(rule["parent"])
        principle = principles_by_id.get(principle_id, {})
        rationale_id = str(principle.get("parent", ""))
        rationale = rationales_by_id.get(rationale_id, {})

        solutions = (
            format_solutions(rule.get("solutions", []))
            + format_solutions(principle.get("solutions", []))
            + format_solutions(rationale.get("solutions", []))
        )
        smells = tuple(" ".join(str(smell).strip().split()) for smell in rule.get("smells", []))
        chains.append(
            RuleChain(
                rule_id=rule_id,
                marker=str(rule["marker"]),
                group=str(rule["group"]),
                principle_id=principle_id,
                rationale_id=rationale_id,
                published_url=f"https://thruput.se/agents/#{slugify_id(rule_id)}",
                smells=smells,
                ancestor_solutions=tuple(solutions),
            )
        )
    return tuple(chains)


def load_declared_standard_ids(upstream_dir: Path) -> set[str]:
    standards_path = upstream_dir / "Standards.yaml"
    if not standards_path.exists():
        return set()
    data = yaml.safe_load(standards_path.read_text(encoding="utf-8"))
    return {str(item["id"]) for item in data.get("standards", [])}


def parse_matrix_rule_ids(matrix_path: Path) -> list[str]:
    content = matrix_path.read_text(encoding="utf-8")
    return re.findall(r"^\| `([^`]+)` \|", content, flags=re.MULTILINE)


def audit_repository(upstream_dir: Path, repo_root: Path) -> SyncAuditReport:
    chains = load_rule_chains(upstream_dir)
    valid_ids = {chain.rule_id for chain in chains} | load_declared_standard_ids(upstream_dir)

    matrix_ids = parse_matrix_rule_ids(repo_root / "docs" / "rule-detection-matrix.md")
    upstream_rule_ids = [chain.rule_id for chain in chains]
    matrix_id_set = set(matrix_ids)
    upstream_rule_set = set(upstream_rule_ids)

    removed_from_matrix = tuple(rid for rid in matrix_ids if rid not in upstream_rule_set)
    missing_from_matrix = tuple(rid for rid in upstream_rule_ids if rid not in matrix_id_set)

    orphaned = []
    unmapped = []
    severity_mismatches = []

    for rule_group in RULE_DIRS:
        rules_root = repo_root / rule_group / "rules"
        if not rules_root.is_dir():
            continue
        for rule_file in sorted(rules_root.rglob("*.yaml")):
            rel_path = rule_file.relative_to(repo_root).as_posix()
            doc = yaml.safe_load(rule_file.read_text(encoding="utf-8"))
            for entry in doc.get("rules", []):
                semgrep_id = str(entry.get("id", ""))
                metadata = entry.get("metadata", {})
                mapped_rule = str(metadata.get("rule", "")).strip()
                mapped_smell = str(metadata.get("smell", "")).strip()
                severity = str(entry.get("severity", "")).strip()

                if not mapped_rule:
                    unmapped.append(f"{rel_path}::{semgrep_id}")
                elif mapped_rule not in valid_ids:
                    orphaned.append(f"{rel_path}::{semgrep_id}::{mapped_rule}")

                if mapped_smell and severity != "WARNING":
                    severity_mismatches.append(f"{rel_path}::{semgrep_id}::{severity}")

    return SyncAuditReport(
        removed_from_matrix=removed_from_matrix,
        missing_from_matrix=missing_from_matrix,
        orphaned_semgrep_rules=tuple(orphaned),
        unmapped_semgrep_rules=tuple(unmapped),
        smell_severity_mismatches=tuple(severity_mismatches),
        rule_chains=chains,
    )


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/sync_audit.py <upstream-rules-dir> [--strict]", file=sys.stderr)
        return 2
    upstream_dir = Path(sys.argv[1]).resolve()
    strict_mode = "--strict" in sys.argv[2:]
    repo_root = Path(__file__).resolve().parent.parent
    report = audit_repository(upstream_dir, repo_root)
    print(json.dumps(asdict(report), indent=2))
    if strict_mode and (
        report.removed_from_matrix
        or report.missing_from_matrix
        or report.orphaned_semgrep_rules
        or report.unmapped_semgrep_rules
        or report.smell_severity_mismatches
    ):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
