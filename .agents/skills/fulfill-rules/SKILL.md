---
name: fulfill-rules
description: Synchronize and fulfill updated, added, or refined rules from https://thruput.se/agents across all supported target languages in thruput-io/semgrep. Trigger when the user asks to fulfill rules, sync rules from https://thruput.se/agents, or update Semgrep rules after upstream rule refinements.
---

# Fulfill Rules (`fulfill-rules`)

When upstream rules at [`https://thruput.se/agents`](https://thruput.se/agents) are added, refined, or recategorized, use this skill to bring `thruput-io/semgrep` into full alignment across [`docs/rule-detection-matrix.md`](../../docs/rule-detection-matrix.md) and every supported language directory (`python/`, `csharp/`, `bash/`, `javascript/`).

## 1. Read the Upstream Source of Truth

1. Read the authoritative rules and glossary definitions from the single source of truth at [`https://thruput.se/agents/rules/Rules.yaml`](https://thruput.se/agents/rules/Rules.yaml) and [`https://thruput.se/agents/rules/Definitions.yaml`](https://thruput.se/agents/rules/Definitions.yaml).
2. Read [`docs/rule-detection-matrix.md`](../../docs/rule-detection-matrix.md) to compare the upstream rules against the current repository matrix.
3. Diff [`https://thruput.se/agents/rules/Rules.yaml`](https://thruput.se/agents/rules/Rules.yaml) against `docs/rule-detection-matrix.md` across four dimensions:
   - **New rules**: Present in `https://thruput.se/agents/rules/Rules.yaml` but missing from `docs/rule-detection-matrix.md`.
   - **Removed or renamed rules**: Present in the matrix or `<lang>/rules/` but removed or renamed in `https://thruput.se/agents/rules/Rules.yaml`.
   - **Refined specifications or `bad`/`good` examples**: Changes to `specification`, `why`, `parent`, `marker`, or code examples in `https://thruput.se/agents/rules/Rules.yaml`.
   - **Detection score changes**: Evaluate whether a new or refined rule scores **`>= 8` on the `Semgrep (1–10)` axis** (syntactic or file-local structural patterns detectable with low false-positive rates).

## 2. Update `docs/rule-detection-matrix.md`

1. Score any newly added or structurally changed rules across the three detection mechanisms (`Semgrep`, `Arch-Test`, `AI-Reasoning`) on the `1–10` scale defined in [`docs/rule-detection-matrix.md`](../../docs/rule-detection-matrix.md).
2. Update the per-group tables and summary counts so every rule at `https://thruput.se/agents` is accounted for.
3. Identify the target implementation set: **all rules with `Semgrep >= 8`** (unless the user explicitly specifies a different score threshold or subset).

## 3. Audit Coverage Across Supported Languages

Discover all supported language directories by inspecting `get_all_rule_files()` in [`tests/test_all_rules.py`](../../tests/test_all_rules.py).

For each rule scoring `Semgrep >= 8` and each supported language `<lang>`:
1. Determine whether the rule applies to `<lang>` (for example, `Use strict presets` applies to languages with compiler/interpreter strictness flags or headers; `Scripts abort on unhandled error` applies to scripting/CLI languages).
2. Map the rule's `parent` group at `https://thruput.se/agents` to the corresponding category directory under `<lang>/rules/<category>/`:
   - `purpose-and-accuracy`
   - `architecture-and-design`
   - `dead-code-and-comments`
   - `domain-modeling`
   - `encapsulation-and-boundaries`
   - `behavior-and-failure-handling`
   - `testing`
   - `quality-tooling`
3. Check whether `<lang>/rules/<category>/<rule-slug>.yaml` and its paired fixture `<lang>/rules/<category>/<rule-slug>.<ext>` exist and match the latest upstream specification and examples.

## 4. Create or Update Rule YAML & Test Fixtures

For every missing or outdated rule in `<lang>/rules/<category>/<rule-slug>.yaml`:

1. **Rule YAML contract** (enforced by `TestRulesStructureAndSchema` in `tests/test_all_rules.py`):
   - `id`: `<rule-slug>` (must be non-empty and match the annotations in the paired fixture).
   - `message`: Concise explanation of the violation and the required remedy, grounded in `specification` and `why` at `https://thruput.se/agents`.
   - `severity`: `ERROR` for `MUST` / `MUST NOT` rules; `WARNING` for `SHOULD` / `SHOULD NOT` rules.
   - `languages`: Semgrep language list (e.g. `[python]`, `[csharp]`, `[bash]`, `[javascript]`).
   - `metadata`: Must include `category` (and optionally `cwe` or `references`).
2. **Paired test fixture (`<rule-slug>.<ext>`)** (enforced by `TestPerRulePositiveAndNegativeCases` in `tests/test_all_rules.py`):
   - Must contain **at least 1 positive case** annotated with `ruleid: <rule-slug>` within 3 lines above the finding (`assert_rule_triggers_near`).
   - Must contain **at least 1 negative case** annotated with `ok: <rule-slug>` within 3 lines above safe code (`assert_rule_silent_near`).
   - For whole-file threshold rules such as `max-file-lines`, keep `<rule-slug>.<ext>` as the positive fixture (201 lines with `ruleid: max-file-lines` before line 201) and place the negative fixture in `<rule-slug>.ok.<ext>` (`resolve_fixture_files` automatically pairs `.ok.<ext>` as the negative fixture).
3. **Keep files under 200 lines**: Every file (except `max-file-lines.<ext>` positive fixtures) must be `<= 200` lines to comply with `File too large`.

## 5. Validate, Test, and Scan Real Code

Run these checks in order before opening a PR:

1. **Validate rule syntax**:
   ```bash
   semgrep scan --validate --config <lang>/rules
   ```
2. **Run inline Semgrep rule tests**:
   ```bash
   semgrep test <lang>/rules
   ```
3. **Run the repository test suite**:
   ```bash
   pytest -v
   ```
4. **Dogfood against real code**:
   Run `<lang>/bin/semgrep-<lang>` against real files in this repository or `.agents/skills/` to confirm precision and eliminate false positives on legitimate idioms.
