# Rule Detection Matrix: Semgrep vs. Arch-Test vs. AI-Reasoning

This document scores each of the 77 rules in [`Rules.yaml`](https://github.com/thruput-io/agents/blob/main/rules/Rules.yaml) (1–10) across three enforcement mechanisms, following the **Push tests down the pyramid** principle:

1. **Semgrep (1–10)** — *Single-file AST, syntactic, or regex pattern matching*
   - **8–10**: Purely syntactic or file-local AST check with high precision (e.g., forbidden syntax, pragmas, comments, file line count, empty catch blocks, skipped test annotations, branching in tests).
   - **4–7**: Catchable as syntactic smells or partial heuristics (e.g., public setters, nullable parameters, platform checks), though cross-file context or semantic exceptions exist.
   - **1–3**: Cannot be detected via single-file syntax without extreme false positives or false negatives.
2. **Arch-Test (1–10)** — *Reflection, type-system graph, and module/assembly dependency inspection (e.g., ArchUnit, NetArchTest, import-linter, AST/reflection test suites)*
   - **8–10**: Cross-module or reflection-level structural invariants (e.g., layer dependency direction, private constructors, domain immutability, domain-only method signatures, no primitives crossing layer boundaries).
   - **4–7**: Partially verifiable by inspecting type signatures, test fixture imports, or call graphs across modules.
   - **1–3**: Either purely local syntax (better handled by Semgrep) or purely semantic/intent-driven.
3. **AI-Reasoning (1–10)** — *Semantic intent, business purpose alignment, PR diff correlation, and architectural judgment*
   - **8–10**: Requires understanding human/business intent, evaluating whether code solves only the stated purpose, judging reuse vs. platform/library choices, assessing test pyramid placement, or correlating code diffs against PR descriptions, ADRs, and telemetry.
   - **4–7**: Complements static tools by catching semantic evasions where syntactic/structural checks only cover common idioms.
   - **1–3**: Deterministic check already solved by Semgrep or Arch-Test.

---

## 1. Purpose

| Rule | Semgrep | Arch-Test | AI-Reasoning | How It Is Caught / Rationale |
| :--- | :---: | :---: | :---: | :--- |
| `Stated purpose` | 1 | 1 | **10** | Requires reading PR description/commit/issue to verify a stated user benefit exists. |
| `No code without purpose` | 1 | 1 | **10** | Requires mapping PR diff existence to a stated purpose. |
| `Every part solves the Purpose` | 1 | 1 | **10** | Semantic traceability between each hunk in a diff and the stated goal. |
| `Nothing beyond the Purpose` | 1 | 1 | **10** | Detecting scope creep or unrelated changes requires semantic diff review. |
| `No speculative portability` | **9** | 2 | 6 | OS/shell branching (`uname`, `sys.platform`, `RuntimeInformation.IsOSPlatform`) is caught by Semgrep ([`no-speculative-portability.yaml`](../bash/rules/purpose-and-accuracy/no-speculative-portability.yaml), [`no-speculative-platform-branching.yaml`](../python/rules/purpose-and-accuracy/no-speculative-platform-branching.yaml)). |

## 2. Reuse

| Rule | Semgrep | Arch-Test | AI-Reasoning | How It Is Caught / Rationale |
| :--- | :---: | :---: | :---: | :--- |
| `No platform feature where reuse serves` | 2 | 3 | **9** | Requires knowing what utilities/components already exist across the codebase. |
| `No dependency where the platform serves` | 2 | 4 | **9** | Requires comparing new package imports against standard library capabilities. |
| `No external service where a dependency serves` | 1 | 2 | **10** | Architectural evaluation of in-process library vs. external service. |
| `No new code where an external tool serves` | 1 | 1 | **10** | Requires ecosystem knowledge of existing tools vs. custom implementation. |
| `Available` | 1 | 2 | **9** | Evaluating license models, commercial restrictions, and extra runtime stacks. |
| `Maintained` | 1 | 2 | **9** | Requires checking external repository activity, contributor count, and documentation. |
| `No second representation` | 2 | 4 | **9** | Detecting duplicated domain knowledge across code, config, and schemas. |

## 3. Conventions

| Rule | Semgrep | Arch-Test | AI-Reasoning | How It Is Caught / Rationale |
| :--- | :---: | :---: | :---: | :--- |
| `Consistent with the codebase` | 3 | 5 | **9** | Comparing naming, idioms, and patterns against surrounding files. |
| `Demonstrable, not recalled` | 1 | 1 | **10** | Verifying citations and standards in prose, reviews, and ADRs. |
| `File too large` | **10** | 4 | 1 | Enforced deterministically via line-count pattern in Semgrep ([`max-file-lines.yaml`](../python/rules/quality-tooling/max-file-lines.yaml)). |
| `No comments in code` | **10** | 1 | 2 | Enforced deterministically by Semgrep comment rules with machine-read exemptions ([`no-comments-in-code.yaml`](../bash/rules/dead-code-and-comments/no-comments-in-code.yaml), [`no-comments.yaml`](../python/rules/dead-code-and-comments/no-comments.yaml)). |
| `No unstated standard` | 2 | 1 | **9** | Auditing agent prompt/rule files against entries in `Rules.yaml`. |

## 4. Types

| Rule | Semgrep | Arch-Test | AI-Reasoning | How It Is Caught / Rationale |
| :--- | :---: | :---: | :---: | :--- |
| `Validating factory` | 4 | **9** | 6 | Arch-Test verifies domain types expose static factory methods; AI verifies invariants are checked. |
| `Private constructor` | 6 | **10** | 2 | Reflection/Arch-Test deterministically asserts all constructors on domain classes are `private`. |
| `Creation failure in the signature` | 5 | **8** | 6 | Arch-Test checks factory return types (e.g., `Result<T, E>`); Semgrep flags `throw` inside factories. |
| `Sum types` | 3 | 6 | **8** | AI + Arch-Test identify product types with multiple optional fields that model mutually exclusive states. |
| `Enums for domain states` | 4 | 6 | **8** | AI identifies boolean/string flags representing domain lifecycle states; Arch-Test bans `bool`/`string` state properties. |
| `Compile-time optionality` | **7** | 6 | 5 | Semgrep catches runtime null/None checks ([`compare-none-equality.yaml`](../python/rules/domain-modeling/compare-none-equality.yaml), [`compare-null-equality.yaml`](../csharp/rules/domain-modeling/compare-null-equality.yaml)). |
| `Wrap primitives` | 5 | **9** | 5 | Arch-Test inspects public method signatures in the domain namespace for raw primitives (`string`, `int`, `Guid`). |

## 5. Domain Model

| Rule | Semgrep | Arch-Test | AI-Reasoning | How It Is Caught / Rationale |
| :--- | :---: | :---: | :---: | :--- |
| `Exhaustive matching` | **8** | 3 | 4 | Semgrep matches `case _:` in Python or `_ =>` / `default:` in C# `switch` expressions/statements. |
| `Self-guarding aggregates` | **7** | **9** | 5 | Semgrep & Arch-Test ban public setters and mutable collection properties ([`no-public-mutable-collection-properties.yaml`](../csharp/rules/domain-modeling/no-public-mutable-collection-properties.yaml)). |
| `No mutators` | **8** | **10** | 3 | Semgrep flags public setters and non-frozen models ([`csharp-no-public-setters.yaml`](../csharp/rules/domain-modeling/csharp-no-public-setters.yaml), [`enforce-frozen-dataclasses.yaml`](../python/rules/domain-modeling/enforce-frozen-dataclasses.yaml)); Arch-Test verifies immutability across domain types. |
| `No unwrapping` | **7** | **8** | 5 | Semgrep flags `.value` access on domain primitives ([`no-unwrapping-domain-primitives.yaml`](../python/rules/domain-modeling/no-unwrapping-domain-primitives.yaml)); Arch-Test restricts unwrapping to perimeter adapters. |
| `Strong typing` | **7** | **8** | 7 | Semgrep bans `Any`, `dynamic`, `object`, and dict subclasses ([`ban-any-in-domain-signatures.yaml`](../python/rules/domain-modeling/ban-any-in-domain-signatures.yaml), [`ban-dynamic-and-object.yaml`](../csharp/rules/domain-modeling/ban-dynamic-and-object.yaml)). |
| `Domain-only interfaces` | 3 | **10** | 4 | Classic Arch-Test rule: every public method on a domain object (except its factory) only accepts/returns domain types. |
| `Domain operations` | 4 | 6 | **8** | AI reasoning spots arithmetic/comparison logic done externally instead of through a domain method. |
| `Respect layering` | 4 | **10** | 2 | Textbook Arch-Test / `import-linter` rule enforcing dependency direction across layers. |
| `No primitive leakage` | 3 | **10** | 4 | Arch-Test inspects layer boundary interfaces (Application/Domain/Infrastructure) for primitive types in signatures. |

## 6. Dead Code

| Rule | Semgrep | Arch-Test | AI-Reasoning | How It Is Caught / Rationale |
| :--- | :---: | :---: | :---: | :--- |
| `Delete unused` | 4 | **7** | **7** | Call-graph / dead-code analyzers find unreferenced symbols; AI identifies obsolete helpers/tests in diffs. |

## 7. Failure Handling

| Rule | Semgrep | Arch-Test | AI-Reasoning | How It Is Caught / Rationale |
| :--- | :---: | :---: | :---: | :--- |
| `No silent catch` | **9** | 2 | 4 | Caught by Semgrep ([`empty-catch-block.yaml`](../csharp/rules/behavior-and-failure-handling/empty-catch-block.yaml), [`bare-except.yaml`](../python/rules/behavior-and-failure-handling/bare-except.yaml), [`no-silent-catch.yaml`](../bash/rules/behavior-and-failure-handling/no-silent-catch.yaml)). |
| `No default on failure` | **9** | 2 | 5 | Caught by Semgrep (`except: return default`, `${var:-default}`, `|| echo default` in [`no-fallback-return-in-except.yaml`](../python/rules/behavior-and-failure-handling/no-fallback-return-in-except.yaml), [`no-default-on-failure.yaml`](../bash/rules/behavior-and-failure-handling/no-default-on-failure.yaml)). |
| `No strategy fallback` | 4 | 2 | **9** | Multi-method/multi-endpoint fallback chains are structural/semantic and best recognized by AI reasoning. |
| `No suppressed exit status` | **9** | 1 | 3 | Caught by Semgrep (`|| true`, `check=False`, `set +e` in [`no-suppressed-exit-status.yaml`](../bash/rules/behavior-and-failure-handling/no-suppressed-exit-status.yaml), [`subprocess-require-check.yaml`](../python/rules/behavior-and-failure-handling/subprocess-require-check.yaml)). |
| `No discarded diagnostics` | **9** | 1 | 4 | Caught by Semgrep (`2>/dev/null`, `stderr=subprocess.DEVNULL` in [`no-discarded-diagnostics.yaml`](../bash/rules/behavior-and-failure-handling/no-discarded-diagnostics.yaml), [`no-subprocess-discard-stderr.yaml`](../python/rules/behavior-and-failure-handling/no-subprocess-discard-stderr.yaml)). |
| `Scripts abort on error` | **10** | 1 | 1 | Caught by Semgrep (`set -euo pipefail` in [`scripts-abort-on-error.yaml`](../bash/rules/behavior-and-failure-handling/scripts-abort-on-error.yaml) and [`no-disabling-errexit.yaml`](../bash/rules/behavior-and-failure-handling/no-disabling-errexit.yaml)). |
| `No degraded continuation` | 3 | 2 | **9** | Detecting continuation with partial/stale state across control flow requires AI reasoning. |
| `Linear deterministic code` | **9** | 3 | 4 | Caught by Semgrep in test/build files ([`linear-deterministic-code.yaml`](../bash/rules/testing/linear-deterministic-code.yaml), [`no-branching-or-loops-in-tests.yaml`](../python/rules/testing/no-branching-or-loops-in-tests.yaml)). |

## 8. Tests

| Rule | Semgrep | Arch-Test | AI-Reasoning | How It Is Caught / Rationale |
| :--- | :---: | :---: | :---: | :--- |
| `No muted tests` | **10** | 3 | 1 | Caught by Semgrep (`@pytest.mark.skip`, `[Fact(Skip=...)]`, bats `skip` in [`no-muted-tests.yaml`](../bash/rules/testing/no-muted-tests.yaml), [`no-skipped-or-ignored-tests.yaml`](../python/rules/testing/no-skipped-or-ignored-tests.yaml)). |
| `No coverage-only tests` | **7** | 3 | **8** | Semgrep catches tests with zero assertions ([`test-must-have-assertion.yaml`](../python/rules/testing/test-must-have-assertion.yaml)); AI catches discarded return values. |
| `Assert values` | **8** | 2 | 7 | Semgrep catches status-only or missing assertions ([`assert-values.yaml`](../bash/rules/testing/assert-values.yaml)); AI verifies assertions check meaningful domain values. |
| `Add tests for new code` | 1 | 5 | **9** | Requires inspecting the PR diff to verify new production code has corresponding test cases. |
| `Add tests for updated code` | 1 | 4 | **9** | Requires inspecting the PR diff to verify modified behavior is pinned by updated/new tests. |
| `Troubleshooting unit test` | 1 | 2 | **10** | Requires correlating a bug-fix diff with a unit test that reproduces the exact defect. |
| `No retry on failure` | **9** | 3 | 2 | Semgrep matches `@pytest.mark.flaky`, `reraise`, `[Retry]`, or CI test retry flags. |
| `One subject under test` | 3 | **7** | **8** | Arch-Test/AI inspects unit tests instantiating multiple concrete domain services/components. |
| `No test case coupling` | **7** | 6 | 6 | Semgrep catches explicit test ordering attributes ([`no-test-case-ordering.yaml`](../python/rules/testing/no-test-case-ordering.yaml)); Arch-Test/AI detects shared mutable state across tests. |
| `Integration Tests Are Black-Box` | 3 | **9** | 6 | Arch-Test verifies integration test projects only reference public API/contract assemblies and not internal domain/repository internals. |

## 9. Test Pyramid

| Rule | Semgrep | Arch-Test | AI-Reasoning | How It Is Caught / Rationale |
| :--- | :---: | :---: | :---: | :--- |
| `No check the type system makes` | **7** | 5 | **8** | Semgrep catches `isinstance`/null checks on typed parameters; AI identifies tests that only test type/null rejection. |
| `No test a linter makes` | 2 | 4 | **9** | AI evaluates whether a written test duplicates a static analysis / linter check. |
| `No narrow integration test for a unit` | 1 | 4 | **9** | AI evaluates whether container/IO fixtures are stood up to test pure in-memory business logic. |
| `No integration test for one component` | 1 | 5 | **9** | AI + Arch-Test check if a full-service integration test only exercises a single adapter. |
| `No end-to-end test for one service` | 1 | 4 | **9** | AI evaluates whether an E2E test only verifies a single service boundary. |
| `No manual test for an automated one` | 1 | 1 | **10** | AI reviews PR descriptions/test plans that defer automated verification to manual testing. |

## 10. Toolchain & Environment

| Rule | Semgrep | Arch-Test | AI-Reasoning | How It Is Caught / Rationale |
| :--- | :---: | :---: | :---: | :--- |
| `Test setup leaves production code alone` | 5 | **8** | **8** | Arch-Test ensures production assemblies have zero test references/hooks; Semgrep flags test environment branches in production code. |
| `No global lint changes` | 2 | 5 | **9** | Diff-level check verifying lint config files are not modified alongside feature code. |
| `No global quality changes` | 2 | 5 | **9** | Diff-level check verifying quality gate configs are isolated to dedicated PRs. |
| `No local disabling of lint rules` | **10** | 1 | 1 | Caught deterministically by Semgrep (`# noqa`, `# pragma: no cover`, `#pragma warning disable`, `[SuppressMessage]`, `# shellcheck disable` in [`no-disabling-via-pragma.yaml`](../bash/rules/quality-tooling/no-disabling-via-pragma.yaml), [`no-linter-pragma-disables.yaml`](../python/rules/quality-tooling/no-linter-pragma-disables.yaml), [`no-suppress-message-attribute.yaml`](../csharp/rules/quality-tooling/no-suppress-message-attribute.yaml)). |
| `No committing generated code` | **8** | 5 | 4 | Semgrep matches generated-file banners (`@generated`, `<auto-generated>`) and build artifacts in source trees. |
| `Strict presets` | **8** | 5 | 4 | Semgrep/config rules scan `pyproject.toml`, `.csproj` (`TreatWarningsAsErrors`), `tsconfig.json` (`strict: true`). |
| `One-command setup` | 1 | 3 | **9** | AI inspects `README.md`, `Makefile`, and CI workflows to verify single-command build/test. |
| `No manual environment setup` | 1 | 2 | **9** | AI inspects documentation and infrastructure scripts for manual provisioning instructions. |
| `Twice is automated` | 1 | 1 | **10** | AI detects runbooks/checklists documenting manual steps instead of scripts. |
| `Ship with telemetry` | 2 | 4 | **9** | AI correlates new production behaviors/endpoints in a diff with structured logging/metrics/traces. |

## 11. Contracts

| Rule | Semgrep | Arch-Test | AI-Reasoning | How It Is Caught / Rationale |
| :--- | :---: | :---: | :---: | :--- |
| `No optionality` | **9** | **9** | 3 | Caught by Semgrep ([`no-nullable-parameters.yaml`](../python/rules/domain-modeling/no-nullable-parameters.yaml), [`no-nullable-constructor-defaults.yaml`](../csharp/rules/domain-modeling/no-nullable-constructor-defaults.yaml)) and Arch-Test reflection over method parameters. |
| `Prefer APIs without optionality` | 2 | 3 | **9** | Requires knowing alternative third-party/framework APIs and their overload signatures. |
| `Overload per option combination` | 6 | **8** | 6 | Semgrep/Arch-Test flags default parameter values and optional args; AI verifies explicit method naming per combination. |
| `Forced optionality at perimeter` | 5 | **7** | **8** | Arch-Test ensures `Optional`/`Nullable` types never leave adapter classes; AI verifies immediate folding at the call statement. |
| `Accept unknown properties` | **8** | **7** | 4 | Semgrep/Arch-Test checks serializer settings (e.g., banning `extra="forbid"` or `JsonUnmappedMemberHandling.Disallow` on inbound DTOs). |
| `Generic parameters, specific returns` | 6 | **9** | 4 | Arch-Test inspects method signatures (parameters use `IEnumerable<T>`/`Sequence[T]` while returns use concrete/immutable collection types). |
| `Shapes live in the contract` | 2 | **7** | **8** | Arch-Test checks boundary DTOs derive from contract schemas (OpenAPI/Protobuf); AI spots hand-written boundary shapes in diffs. |

## 12. Performance

| Rule | Semgrep | Arch-Test | AI-Reasoning | How It Is Caught / Rationale |
| :--- | :---: | :---: | :---: | :--- |
| `No iteration over calls over the network` | **7** | 5 | **8** | Semgrep catches direct `http`/`db`/`await client` calls inside `for`/`while` loops; AI catches indirect N+1 network calls across helper methods. |
| `No performance claim without measurement or IO reduction` | 1 | 1 | **10** | AI evaluates PR descriptions/commit messages claiming performance gains against benchmark evidence or network-call reduction. |

---

## Summary Distribution Across the 77 Rules

- **Primary Semgrep Candidates (Score ≥ 7: 23 rules)**: Syntax, pragmas, comments, file size, exception suppression, test annotations, test branching, and local type/nullability smells.
- **Primary Arch-Test Candidates (Score ≥ 7: 19 rules)**: Layering (`Respect layering`), boundary containment (`No primitive leakage`, `Domain-only interfaces`, `Integration Tests Are Black-Box`), constructor visibility (`Private constructor`), and reflection-level signature rules (`Wrap primitives`, `Generic parameters, specific returns`, `No mutators`).
- **Primary AI-Reasoning Candidates (Score ≥ 7: 42 rules)**: Purpose alignment, reuse hierarchy decisions, test pyramid placement, diff-to-test correlation, and cross-method semantic patterns (`No strategy fallback`, `No degraded continuation`).
