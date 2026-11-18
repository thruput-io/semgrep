# 001 — Language-Agnostic Common Rules, Anti-Compacting Guardrails, and Skill-Driven Upstream Rule Sync

|                |                                                                                                      |
|----------------|------------------------------------------------------------------------------------------------------|
| Plan           | `docs/plans/language-agnostic-rules-and-sync/001-language-agnostic-rules-and-sync.md`                |
| Started        | 2026-11-18                                                                                           |
| Supersedes     | —                                                                                                    |
| ADRs consulted | —                                                                                                    |
| ADRs added     | [0001](../../adrs/0001-language-agnostic-common-rules.yaml), [0002](../../adrs/0002-smell-warnings-anti-compacting-and-sync-skill.yaml) |
| Status         | in-progress                                                                                          |

## Implementing Agent Instructions

Read the repository governance (`Rules.yaml`, `Principles.yaml`, `Rationales.yaml`, `Definitions.yaml`, `Axioms.yaml`), ADRs `0001` and `0002`, and this plan before modifying code. Keep each milestone in its own small pull request (`<= 400` lines changed) branched from `main`, write failing tests before implementation, and record milestone verification and commit hashes in `docs/plans/language-agnostic-rules-and-sync/progress/001-attempt-1-2026-11-18.md`.

## Background

Upstream governance (`thruput-io/agents`) replaced standalone `File too large` with the `Single-purpose components` rule and its 200-line smell, folded overlapping rules into smells (`No unwrapping`, `No coverage-only tests`, `No code without purpose`, `Nothing beyond the Purpose`, `No primitive leakage`, `No global lint changes`), renamed `Enums for domain states` (`Closed enumerations`) and `No performance claim without measurement or IO reduction` (`No performance motivations on in-memory operations`), and expanded `SHOULD`/`MAY` solutions across the hierarchy.

Meanwhile, `thruput-io/semgrep` duplicated `max-file-lines` across every language at `ERROR` severity with test-path exemptions, lacked guardrails against agents compacting code horizontally or packing statements onto single lines to game the 200-line threshold, and retained rules removed upstream or unsuited for high-precision single-file Semgrep matching.

## Goals

1. **Shared `common/rules/` architecture (ADR 0001):**
   - Author language-agnostic rules once under `common/rules/` (`languages: [generic]`), validated in `tests/test_all_rules.py` and CI.
   - Include `common/rules/` once in `all.yaml` / `rules.yaml` / `index.html`, and include `common/rules/` in every per-language bundle (`<lang>.yaml`), CLI wrapper (`semgrep-python`, `semgrep-bash`, `semgrep-javascript`), Python wheel/sdist, and C# NuGet package.
2. **Single-responsibility `max-file-lines` warning + anti-compacting `ERROR` guardrails (ADR 0002):**
   - Replace per-language `max-file-lines` copies with one `common/rules/quality-tooling/max-file-lines.yaml` (`severity: WARNING`, zero test-path exemptions) citing `Single-purpose components`, prescribing decomposition by responsibility (`Separation of Concerns` / `One concern, one owner`), and explicitly prohibiting line compacting.
   - Add `common/rules/quality-tooling/no-line-compacting.yaml` (`severity: ERROR`) catching horizontal code cramming (`> 200` characters on non-URL code lines) and multi-statement single-line semicolon packing (`3+` semicolon-chained statements on one line).
3. **Deterministic upstream audit + `sync-rules` skill + upstream alignment (ADR 0002):**
   - Provide `scripts/sync_audit.py` (covered by `tests/test_sync_audit.py`) to deterministically compare upstream `Rules.yaml`, `Principles.yaml`, and `Rationales.yaml` against `docs/rule-detection-matrix.md` and `metadata.rule` across Semgrep rules.
   - Author `.agents/skills/sync-rules/SKILL.md` guiding upstream synchronization: running `scripts/sync_audit.py`, evaluating Semgrep precision (`>= 8`), placing language-agnostic rules in `common/rules/`, splitting violations only when smells require distinct solutions, and selecting curated solutions from `Rule -> Principle -> Rationale`.
   - Execute `sync-rules` to update `docs/rule-detection-matrix.md` to all 79 upstream rules, remove retired/low-precision Semgrep rules (`no-unwrapping-domain-primitives`, `test-must-have-assertion`, and unmapped heuristic rules), and align canonical `metadata.rule` and solution-oriented messages.

## Execution Plan

### Milestone 1 — ADRs and Persisted Plan (PR Slice 1)
- Author `docs/adrs/0001-language-agnostic-common-rules.yaml` and `docs/adrs/0002-smell-warnings-anti-compacting-and-sync-skill.yaml`, verified against `adr.schema.json` and declared governance IDs.
- Commit this plan and initialize the progress log.

### Milestone 2 — Shared `common/rules/`, `max-file-lines` Warning, and Anti-Compacting Rules (PR Slice 2)
- Write failing tests in `tests/test_all_rules.py`, `tests/test_bundle_rules.py`, and CLI tests for `common/rules/`, `max-file-lines` (`WARNING`, no test exemptions), and `no-line-compacting` (`ERROR`).
- Implement `common/rules/quality-tooling/max-file-lines.yaml` and `common/rules/quality-tooling/no-line-compacting.yaml` with paired positive/negative fixtures; delete duplicated per-language `max-file-lines` files.
- Wire `common/rules/` into `scripts/bundle_rules.py`, `python/` (`setup.py` sdist/wheel + `semgrep_rules` CLI), `csharp/Thruput.Semgrep.Rules.csproj`, `bash/bin/semgrep-bash`, `javascript/bin/semgrep-javascript`, and `.github/workflows/ci.yml`.
- Verify all unit, CLI, bundle, Python build, and C# rule suites pass.

### Milestone 3 — `scripts/sync_audit.py`, `sync-rules` Skill, and Upstream Rule Sync (PR Slice 3)
- Write failing unit tests in `tests/test_sync_audit.py` for upstream delta detection (added/removed rules, smells, ancestor solutions, orphaned `metadata.rule` entries, and severity checks).
- Implement `scripts/sync_audit.py` and `.agents/skills/sync-rules/SKILL.md` (fixing stale upstream URLs in `.agents/skills/add-language/SKILL.md` as well).
- Run `sync-rules`: update `docs/rule-detection-matrix.md` to the 79 upstream rules, prune retired and low-precision Semgrep rules + fixtures, and enrich retained rules with canonical `metadata.rule` and concise solution guidance.
- Verify `pytest` and `semgrep scan --validate` pass across the repository.

## Goal Coverage

| Goal | Covered By |
|------|------------|
| 1. Shared `common/rules/` architecture | Milestone 1, Milestone 2 |
| 2. `max-file-lines` `WARNING` (no exemptions) + anti-compacting `ERROR` rules | Milestone 2 |
| 3. Deterministic `sync_audit.py` + `sync-rules` skill + upstream sync & pruning | Milestone 3 |
