from dataclasses import dataclass
from pathlib import Path
import sys
import yaml

LANGUAGES: tuple[str, ...] = ("python", "csharp", "bash", "javascript")


@dataclass(frozen=True)
class RulesetBundle:
    serialized_yaml: str
    rule_count: int


def collect_language_bundle(repo_root: Path, language: str) -> RulesetBundle:
    rules_dir = repo_root / language / "rules"
    rule_files = sorted(rules_dir.rglob("*.yaml"))
    collected = []
    for rule_file in rule_files:
        with open(rule_file, "r", encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        for entry in data["rules"]:
            collected.append({**entry, "id": str(entry["id"])})
    serialized = yaml.safe_dump({"rules": collected}, sort_keys=False, allow_unicode=True)
    return RulesetBundle(serialized_yaml=serialized, rule_count=len(collected))


def collect_combined_bundle(repo_root: Path) -> RulesetBundle:
    combined = []
    for language in LANGUAGES:
        rules_dir = repo_root / language / "rules"
        for rule_file in sorted(rules_dir.rglob("*.yaml")):
            with open(rule_file, "r", encoding="utf-8") as handle:
                data = yaml.safe_load(handle)
            for entry in data["rules"]:
                raw_id = str(entry["id"])
                qualified_id = raw_id if raw_id.startswith(f"{language}.") else f"{language}.{raw_id}"
                combined.append({**entry, "id": qualified_id})
    serialized = yaml.safe_dump({"rules": combined}, sort_keys=False, allow_unicode=True)
    return RulesetBundle(serialized_yaml=serialized, rule_count=len(combined))


def write_bundle(target_path: Path, bundle: RulesetBundle) -> None:
    target_path.write_text(bundle.serialized_yaml, encoding="utf-8")


def bundle_all_rulesets(repo_root: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    for language in LANGUAGES:
        lang_bundle = collect_language_bundle(repo_root, language)
        write_bundle(output_dir / f"{language}.yaml", lang_bundle)
    combined_bundle = collect_combined_bundle(repo_root)
    write_bundle(output_dir / "all.yaml", combined_bundle)
    write_bundle(output_dir / "rules.yaml", combined_bundle)
    write_bundle(output_dir / "index.html", combined_bundle)


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent
    out_arg = sys.argv[1] if len(sys.argv) > 1 else str(repo_root / "dist" / "site")
    bundle_all_rulesets(repo_root, Path(out_arg))
    return 0


if __name__ == "__main__":
    sys.exit(main())
