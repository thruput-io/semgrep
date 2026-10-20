---
name: add-language
description: Onboard a new target programming language into thruput-io/semgrep, including rule authoring for rules scoring >= 8 in docs/rule-detection-matrix.md, paired positive/negative fixtures, CLI wrapper, test registration, CI job, and real-corpus validation.
---

# Add a Target Language (`add-language`)

Use this skill when adding support for a new programming language `<lang>` to `thruput-io/semgrep`.

## 1. Select Rules to Implement

1. Read [`docs/rule-detection-matrix.md`](../../docs/rule-detection-matrix.md) and the authoritative rules at [`https://thruput.se/agents/rules/Rules.yaml`](https://thruput.se/agents/rules/Rules.yaml).
2. By default, select all rules scoring **`>= 8` in `Semgrep (1–10)`** (the high-precision syntactic/AST tier), unless the user specifies a different score threshold:
   - `purpose-and-accuracy`: `no-speculative-portability`
   - `dead-code-and-comments`: `no-comments-in-code`
   - `domain-modeling`: `exhaustive-matching`, `no-mutators`, `no-optionality`, `accept-unknown-properties`
   - `behavior-and-failure-handling`: `no-silent-catch`, `no-default-on-failure`, `no-suppressed-exit-status`, `no-discarded-diagnostics`, `scripts-abort-on-error`
   - `testing`: `linear-deterministic-code`, `no-muted-tests`, `assert-values`, `no-retry-on-failure`
   - `quality-tooling`: `max-file-lines`, `no-disabling-via-pragma`, `no-committing-generated-code`, `strict-presets`
3. Translate each generic rule concept into the **idiomatic failure modes and standard libraries** of `<lang>` (for example, in JavaScript: `node:test`, `node:assert/strict`, `child_process`, `zod`/`ajv`, `eslint-disable`/`@ts-ignore`, and ES module patterns).

## 2. Directory & File Layout

Create the following layout under `<lang>/`:

```text
<lang>/
├── bin/
│   └── semgrep-<lang>          # Executable wrapper script (chmod +x)
└── rules/
    └── <category>/
        ├── <rule-slug>.yaml    # Rule definition
        └── <rule-slug>.<ext>   # Paired test fixture (ruleid + ok annotations)
```

### Rule YAML & Fixture Requirements
- `id`: `<rule-slug>`
- `languages`: `[<semgrep-lang-id>]`
- `severity`: `ERROR` (`MUST` / `MUST NOT`) or `WARNING` (`SHOULD` / `SHOULD NOT`)
- `metadata`: Must include `category`.
- Every `ruleid: <rule-slug>` annotation in `<rule-slug>.<ext>` MUST be within 3 lines above the triggered line (`assert_rule_triggers_near` in `tests/test_all_rules.py`).
- Every file (except `max-file-lines.<ext>`) MUST be `<= 200` lines and contain no comments other than machine-read directives (`ruleid:`, `ok:`, shebangs).

## 3. Semgrep AST & Pattern Pitfalls to Avoid

When writing patterns for a new language, verify how Semgrep's parser lowers `<lang>` syntax:

1. **Import propagation rewrites function calls**:
   In languages like JS/TS/Python, importing a symbol (`import { execSync } from 'node:child_process'`) causes Semgrep to resolve `execSync(...)` to `'node:child_process'.execSync(...)`. When matching string-literal shell anti-patterns (such as `|| true` or `2>/dev/null`), prefer `pattern-regex` or provide patterns that match both bare and module-qualified calls.
2. **Module path prefix equivalence**:
   Semgrep treats `import x from 'node:assert'` as matching `import x from 'node:assert/strict'`. Use `pattern-regex` when an exact module specifier without subpaths must be distinguished.
3. **Multi-line construct reporting lines**:
   A class-level pattern like `class $C { ... set $P($V) { ... } ... }` reports findings on the `class` declaration line rather than the `set` method line, breaking the 3-line proximity check in `assert_rule_triggers_near`. Anchor directly on the method or setter line so inline `ruleid:` annotations and PR review comments land on the exact offending line.
4. **Statement-list ellipsis in `switch` / `match` blocks**:
   In JS/TS, `switch ($E) { ... }` is invalid Semgrep pattern syntax; always include a case clause (`switch ($E) { case $V: ... }`).
5. **Whole-file regex rules (`max-file-lines`)**:
   Because `max-file-lines` fires on line 201, any negative lines appended to the same file would push its length past 200 lines. Keep `<rule-slug>.<ext>` at 201 lines for the positive test and place the negative test in `<rule-slug>.ok.<ext>`.

## 4. Create the CLI Wrapper (`<lang>/bin/semgrep-<lang>`)

Create `<lang>/bin/semgrep-<lang>` (`chmod +x`) modelled after [`javascript/bin/semgrep-javascript`](../../javascript/bin/semgrep-javascript) and [`bash/bin/semgrep-bash`](../../bash/bin/semgrep-bash):
- Use `#!/usr/bin/env bash` and `set -euo pipefail`.
- Resolve `rules_path` relative to `BASH_SOURCE[0]`, default target to `"."` when no positional path is passed, and `exec semgrep --error --config "${rules_path}" "${args[@]}"`.

## 5. Register the Language in Tests, CI, and Docs

1. **[`tests/test_all_rules.py`](../../tests/test_all_rules.py)**:
   Add `<LANG>_RULES_ROOT` to `get_all_rule_files()` and add `<lang>`'s fixture file extensions to `resolve_fixture_files(base)`.
2. **`tests/test_<lang>_cli.py`**:
   Add CLI integration tests modelled after [`tests/test_javascript_cli.py`](../../tests/test_javascript_cli.py) verifying executable permissions, violation detection on `BAD_FIXTURE`, zero findings on `OK_FIXTURE`, default `"."` target, and missing `semgrep` error handling.
3. **[`.github/workflows/ci.yml`](../../.github/workflows/ci.yml)** and **[`README.md`](../../README.md)**:
   Add `<lang>/rules` to `semgrep test` in CI and document the new language and rule counts in `README.md`.

## 6. Validate Against a Real Code Corpus

Before raising a PR:
1. Run `semgrep scan --validate --config <lang>/rules` and `semgrep test <lang>/rules`.
2. Run `<lang>/bin/semgrep-<lang>` against a real corpus of `<lang>` files (such as `.agents/skills/pr-review/scripts/` or a target project) to verify that findings are genuine violations and that clean idioms produce zero false positives.
