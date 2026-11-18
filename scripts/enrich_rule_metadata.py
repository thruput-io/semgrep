from dataclasses import dataclass
from pathlib import Path
import sys
import yaml

from scripts.sync_audit import RULE_DIRS, load_rule_chains


@dataclass(frozen=True)
class CuratedMapping:
    rule_id: str
    smell: str
    solution_substrings: tuple[str, ...]


RULE_MAPPINGS: tuple[tuple[str, CuratedMapping], ...] = (
    ("bare-except", CuratedMapping("No silent catch", "", ("safe to kill", "supervisor"))),
    ("empty-catch-block", CuratedMapping("No silent catch", "", ("safe to kill", "supervisor"))),
    ("no-silent-catch", CuratedMapping("No silent catch", "", ("safe to kill", "supervisor"))),
    ("no-fallback-return-in-except", CuratedMapping("No default on failure", "", ("safe to kill", "supervisor"))),
    ("no-default-on-failure", CuratedMapping("No default on failure", "", ("safe to kill", "supervisor"))),
    ("no-subprocess-discard-stderr", CuratedMapping("No discarded diagnostics", "", ("safe to kill", "supervisor"))),
    ("no-discarded-diagnostics", CuratedMapping("No discarded diagnostics", "", ("safe to kill", "supervisor"))),
    ("no-suppressed-shell-exit-codes", CuratedMapping("No suppressed exit status", "", ("safe to kill", "supervisor"))),
    ("subprocess-require-check", CuratedMapping("No suppressed exit status", "", ("safe to kill", "supervisor"))),
    ("no-suppressed-exit-status", CuratedMapping("No suppressed exit status", "", ("safe to kill", "supervisor"))),
    ("scripts-abort-on-error", CuratedMapping("Scripts abort on error", "", ("safe to kill", "supervisor"))),
    ("no-disabling-errexit", CuratedMapping("Scripts abort on error", "", ("safe to kill", "supervisor"))),
    ("require-shebang", CuratedMapping("Scripts abort on error", "", ("safe to kill", "supervisor"))),
    ("no-comments", CuratedMapping("No comments in code", "", ("Name each test",))),
    ("no-comments-in-code", CuratedMapping("No comments in code", "", ("Name each test",))),
    ("ban-any-in-domain-signatures", CuratedMapping("Strong typing", "", ("typing add-on", "introducing encapsulation"))),
    ("ban-dynamic-and-object", CuratedMapping("Strong typing", "", ("typing add-on", "introducing encapsulation"))),
    ("no-dict-subclass-data-bags", CuratedMapping("Strong typing", "", ("typing add-on", "Hide a type's representation"))),
    ("no-dictionary-subclass-data-bags", CuratedMapping("Strong typing", "", ("typing add-on", "Hide a type's representation"))),
    ("enforce-frozen-dataclasses", CuratedMapping("No mutators", "", ("typing add-on", "introducing encapsulation"))),
    ("enforce-frozen-pydantic", CuratedMapping("No mutators", "", ("typing add-on", "introducing encapsulation"))),
    ("csharp-no-public-setters", CuratedMapping("No mutators", "", ("typing add-on", "introducing encapsulation"))),
    ("no-mutators", CuratedMapping("No mutators", "", ("typing add-on", "introducing encapsulation"))),
    ("no-public-mutable-collection-properties", CuratedMapping("Self-guarding aggregates", "", ("collection's invariants", "typing add-on"))),
    ("exhaustive-matching", CuratedMapping("Exhaustive matching", "", ("state machine in the type", "typing add-on"))),
    ("accept-unknown-properties", CuratedMapping("Accept unknown properties", "", ("expanded contract", "Consumer-Driven Contracts"))),
    (
        "max-parameters-warning",
        CuratedMapping(
            "Single-purpose components",
            "A [[Function]] or [[Public method]] with more than 3 parameters.",
            ("Hide each design decision", "Keep concerns separate"),
        ),
    ),
    ("max-parameters-error", CuratedMapping("Single-purpose components", "", ("Hide each design decision", "Keep concerns separate"))),
    ("no-nullable-constructor-defaults", CuratedMapping("No optionality", "", ("Explicitly named method", "strategy"))),
    ("no-nullable-parameters", CuratedMapping("No optionality", "", ("Explicitly named method", "strategy"))),
    ("no-optionality", CuratedMapping("No optionality", "", ("Explicitly named method", "strategy"))),
    ("no-variadic-constructor-args", CuratedMapping("No optionality", "", ("Explicitly named method", "strategy"))),
    ("no-params-in-constructors", CuratedMapping("No optionality", "", ("Explicitly named method", "strategy"))),
    ("no-speculative-platform-branching", CuratedMapping("No speculative portability", "", ("User", "already operates"))),
    ("no-speculative-portability", CuratedMapping("No speculative portability", "", ("User", "already operates"))),
    ("no-linter-pragma-disables", CuratedMapping("No local disabling of lint rules", "", ("root cause", "strictest static-analysis"))),
    ("no-suppress-message-attribute", CuratedMapping("No local disabling of lint rules", "", ("root cause", "strictest static-analysis"))),
    ("no-disabling-via-pragma", CuratedMapping("No local disabling of lint rules", "", ("root cause", "strictest static-analysis"))),
    ("no-committing-generated-code", CuratedMapping("No committing generated code", "", ("same build locally", "root cause"))),
    ("strict-presets", CuratedMapping("Strict presets", "", ("strictest static-analysis", "same build locally"))),
    ("no-branching-or-loops-in-tests", CuratedMapping("Linear deterministic code", "", ("safe to kill", "supervisor"))),
    ("linear-deterministic-code", CuratedMapping("Linear deterministic code", "", ("safe to kill", "supervisor"))),
    ("no-skipped-or-ignored-tests", CuratedMapping("No muted tests", "", ("mutation testing", "painful"))),
    ("no-muted-tests", CuratedMapping("No muted tests", "", ("mutation testing", "painful"))),
    ("no-test-case-ordering", CuratedMapping("No test case coupling", "", ("painful", "tools for verification"))),
    ("assert-values", CuratedMapping("Assert values", "", ("mutation testing", "tools for verification"))),
    ("no-retry-on-failure", CuratedMapping("No retry on failure", "", ("mutation testing", "painful"))),
    (
        "max-file-lines",
        CuratedMapping(
            "Single-purpose components",
            "A [[Component]] longer than 200 lines.",
            ("Hide each design decision", "Keep concerns separate"),
        ),
    ),
    ("no-horizontal-line-cramming", CuratedMapping("Single-purpose components", "", ("Hide each design decision", "Keep concerns separate"))),
    ("no-multi-statement-line-packing", CuratedMapping("Single-purpose components", "", ("Hide each design decision", "Keep concerns separate"))),
)


def resolve_mapping(semgrep_id: str) -> CuratedMapping:
    normalized = semgrep_id
    for prefix in ("python-", "csharp-"):
        if normalized.startswith(prefix) and normalized != "csharp-no-public-setters":
            normalized = normalized[len(prefix):]
    for slug, mapping in RULE_MAPPINGS:
        if normalized == slug:
            return mapping
    raise KeyError(f"No curated mapping declared for Semgrep rule id '{semgrep_id}'")


def select_solutions(ancestor_solutions: tuple[str, ...], substrings: tuple[str, ...]) -> list[str]:
    selected = [
        sol
        for sol in ancestor_solutions
        if any(token in sol for token in substrings)
    ]
    if not selected:
        raise ValueError(f"No ancestor solutions matched substrings {substrings} in {ancestor_solutions}")
    return selected


def enrich_repository_rules(upstream_dir: Path, repo_root: Path) -> int:
    chains_by_id = {chain.rule_id: chain for chain in load_rule_chains(upstream_dir)}
    updated_count = 0

    for group in RULE_DIRS:
        rules_root = repo_root / group / "rules"
        if not rules_root.is_dir():
            continue
        for rule_file in sorted(rules_root.rglob("*.yaml")):
            doc = yaml.safe_load(rule_file.read_text(encoding="utf-8"))
            for entry in doc["rules"]:
                mapping = resolve_mapping(str(entry["id"]))
                chain = chains_by_id[mapping.rule_id]
                meta = dict(entry.get("metadata", {}))
                meta["rule"] = mapping.rule_id
                if mapping.smell:
                    meta["smell"] = mapping.smell
                meta["solutions"] = select_solutions(chain.ancestor_solutions, mapping.solution_substrings)
                existing_refs = [
                    str(ref)
                    for ref in meta.get("references", [])
                    if "RULES.md" not in str(ref) and "rules.yaml" not in str(ref) and "Rules.yaml" not in str(ref)
                ]
                refs = [chain.published_url] + [r for r in existing_refs if r != chain.published_url]
                meta["references"] = refs
                meta.pop("note", None)
                entry["metadata"] = meta
                updated_count += 1
            serialized = yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=120)
            rule_file.write_text(serialized, encoding="utf-8")

    return updated_count


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python scripts/enrich_rule_metadata.py <upstream-rules-dir>", file=sys.stderr)
        return 2
    upstream_dir = Path(sys.argv[1]).resolve()
    repo_root = Path(__file__).resolve().parent.parent
    count = enrich_repository_rules(upstream_dir, repo_root)
    print(f"Enriched {count} Semgrep rule definitions.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
