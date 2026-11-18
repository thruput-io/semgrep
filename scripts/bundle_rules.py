from dataclasses import dataclass
from pathlib import Path
import sys
import yaml

COMMON_RULESET = "common"
LANGUAGES: tuple[str, ...] = ("python", "csharp", "bash", "javascript")


@dataclass(frozen=True)
class RulesetBundle:
    serialized_yaml: str
    rule_count: int


@dataclass(frozen=True)
class LoadedRules:
    yaml_documents: tuple[str, ...]


def read_rule_documents(rules_dir: Path) -> LoadedRules:
    docs = [
        rule_file.read_text(encoding="utf-8")
        for rule_file in sorted(rules_dir.rglob("*.yaml"))
    ]
    return LoadedRules(yaml_documents=tuple(docs))


def build_bundle(loaded: LoadedRules, namespace_prefix: str) -> RulesetBundle:
    collected = []
    for raw_doc in loaded.yaml_documents:
        data = yaml.safe_load(raw_doc)
        for entry in data["rules"]:
            raw_id = str(entry["id"])
            if namespace_prefix and not raw_id.startswith(f"{namespace_prefix}."):
                rule_id = f"{namespace_prefix}.{raw_id}"
            else:
                rule_id = raw_id
            collected.append({**entry, "id": rule_id})
    serialized = yaml.safe_dump({"rules": collected}, sort_keys=False, allow_unicode=True)
    return RulesetBundle(serialized_yaml=serialized, rule_count=len(collected))


def collect_common_bundle(repo_root: Path) -> RulesetBundle:
    return build_bundle(read_rule_documents(repo_root / COMMON_RULESET / "rules"), "")


def collect_language_bundle(repo_root: Path, language: str) -> RulesetBundle:
    lang_docs = read_rule_documents(repo_root / language / "rules").yaml_documents
    common_docs = read_rule_documents(repo_root / COMMON_RULESET / "rules").yaml_documents
    return build_bundle(LoadedRules(yaml_documents=lang_docs + common_docs), "")


def collect_combined_bundle(repo_root: Path) -> RulesetBundle:
    combined = yaml.safe_load(
        build_bundle(
            read_rule_documents(repo_root / COMMON_RULESET / "rules"),
            COMMON_RULESET,
        ).serialized_yaml
    )["rules"]
    for language in LANGUAGES:
        lang_bundle = build_bundle(read_rule_documents(repo_root / language / "rules"), language)
        combined.extend(yaml.safe_load(lang_bundle.serialized_yaml)["rules"])
    serialized = yaml.safe_dump({"rules": combined}, sort_keys=False, allow_unicode=True)
    return RulesetBundle(serialized_yaml=serialized, rule_count=len(combined))


def write_bundle(target_path: Path, bundle: RulesetBundle) -> None:
    target_path.write_text(bundle.serialized_yaml, encoding="utf-8")


def bundle_all_rulesets(repo_root: Path, output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    write_bundle(output_dir / f"{COMMON_RULESET}.yaml", collect_common_bundle(repo_root))
    for language in LANGUAGES:
        write_bundle(output_dir / f"{language}.yaml", collect_language_bundle(repo_root, language))
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
