---
name: sync-rules
description: Synchronize thruput-io/semgrep with upstream governance changes in thruput-io/agents (Rules.yaml, Principles.yaml, Rationales.yaml, Standards.yaml), combining deterministic delta auditing (scripts/sync_audit.py) with agent reasoning to prune retired or low-precision Semgrep rules, place language-agnostic checks in common/rules/, emit smell warnings with anti-gaming guardrails, refine smell-specific violations, and attach curated ancestor solutions.
---

# Synchronize Upstream Governance Rules (`sync-rules`)

Use this skill whenever upstream rules, smells, or solutions change in `thruput-io/agents`.

## 1. Run Deterministic Upstream Delta Audit

1. Fetch the authoritative upstream governance files (`Rules.yaml`, `Principles.yaml`, `Rationales.yaml`, and `Standards.yaml`) from `thruput-io/agents` `main` into a temporary directory:
   ```bash
   TOKEN=$(get-gh-token.sh)
   for f in Rules.yaml Principles.yaml Rationales.yaml Standards.yaml; do
     GH_TOKEN="$TOKEN" gh api "repos/thruput-io/agents/contents/rules/$f" \
       -H 'Accept: application/vnd.github.raw' > "$UPSTREAM_DIR/$f"
   done
   ```
2. Run [`scripts/sync_audit.py`](../../../scripts/sync_audit.py):
   ```bash
   python scripts/sync_audit.py "$UPSTREAM_DIR"
   ```
3. Inspect the five deterministic buckets in the JSON report plus `rule_chains`:
   - `removed_from_matrix`: rules in [`docs/rule-detection-matrix.md`](../../../docs/rule-detection-matrix.md) removed or consolidated upstream.
   - `missing_from_matrix`: newly added upstream rules not yet scored in [`docs/rule-detection-matrix.md`](../../../docs/rule-detection-matrix.md).
   - `orphaned_semgrep_rules`: Semgrep rules whose `metadata.rule` no longer exists upstream.
   - `unmapped_semgrep_rules`: Semgrep rules missing a canonical `metadata.rule`.
   - `smell_severity_mismatches`: Semgrep rules carrying `metadata.smell` whose `severity` is not `WARNING`.

## 2. Evaluate Semgrep Fitness and Prune Retired or Weak Rules (Reasoning)

1. Update [`docs/rule-detection-matrix.md`](../../../docs/rule-detection-matrix.md) so `removed_from_matrix` and `missing_from_matrix` are both empty.
2. Score each new or updated rule (`1–10`) across **Semgrep**, **Arch-Test**, and **AI-Reasoning** per **Push tests down the pyramid**:
   - Keep or author Semgrep rules only where single-file AST or text matching achieves high precision (**score `>= 8`**) without cross-file false positives.
   - Delete Semgrep rule YAMLs and paired fixtures when a rule was retired upstream, contradicts another active rule (such as recommending `None` defaults against `No optionality` or unmeasured in-memory micro-optimizations against `No performance motivations on in-memory operations`), or suffers false positives better handled by Arch-Test or AI-Reasoning.

## 3. Language-Agnostic Placement, Smell Warnings, and Anti-Gaming Guardrails

Follow [ADR 0001](../../../docs/adrs/0001-language-agnostic-common-rules.yaml) and [ADR 0002](../../../docs/adrs/0002-smell-warnings-anti-compacting-and-sync-skill.yaml):

1. **Language-agnostic first (`common/rules/`):**
   Any text-level, line-structure, or universal directive check (`languages: [generic]`) lives once under `common/rules/`, never duplicated per language. Reserve `<lang>/rules/` strictly for language-syntax and AST patterns.
2. **Smell thresholds warn universally (`WARNING`, zero path exemptions):**
   Checks targeting a heuristic `smell` (such as the 200-line threshold on `Single-purpose components`) MUST use `severity: WARNING` with `metadata.smell` set and no test-path `exclude` globs.
3. **Anti-gaming guardrails (`ERROR`):**
   Whenever a heuristic warning could incentivize an AI agent to deform code rather than fix the underlying design smell (for example, compacting lines or chaining statements horizontally to duck 200 lines), pair the warning with deterministic `ERROR` rules in `common/rules/` blocking the gaming behavior.

## 4. Refine Violations by Solution and Attach Ancestor Solutions (Reasoning)

1. **Split violations only when solutions differ:**
   - Split a Semgrep YAML into distinct `rules:` entries when separate `smells` require different remediations (for example, distinct `Comment intent` categories or branching vs fallback defaults).
   - Keep `pattern-either` combined in one rule when all syntax variants share the exact same smell and remediation.
2. **Select curated ancestor solutions:**
   - Inspect `ancestor_solutions` in `sync_audit.py` output (`Rule -> Principle -> Rationale`).
   - Do not dump unrelated rationale solutions verbatim when a broad rationale (such as `Encapsulation`) lists many specialized options; select the 1–3 `SHOULD`/`MAY` solutions that directly remediate the matched violation.
   - Populate `metadata.rule`, optional `metadata.smell`, `metadata.solutions`, and `metadata.references` (`published_url`: `https://thruput.se/agents/#<slug>`), and state both the violated rule/smell and concrete solution concisely in `message`.

## 5. TDD Fixtures and Verification

1. Write or update paired positive (`ruleid:`) and negative (`ok:`) fixtures before finalizing rule patterns.
2. Run `python scripts/sync_audit.py "$UPSTREAM_DIR" --strict`, `pytest`, and `python scripts/bundle_rules.py` to verify all unit, CLI, and bundle suites pass with zero audit mismatches.
