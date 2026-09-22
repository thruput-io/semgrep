# Thruput Semgrep Rules

Curated Semgrep rulesets for **Python** and **.NET (C#)** codebases. All rules are configured with **`ERROR`** severity to enforce strict, blocking quality gates in CI/CD.

---

## 🔄 Development & Verification Workflow

> ### ⚠️ Mandatory Invariant
> **Every single modification must be verified before work is considered complete.**
>
> Never assume a rule pattern or change works without running the test suite. Breaking changes, syntax errors, or unverified patterns are not allowed.

### Rule Modification Requirements:
1. **Severity Policy**: All rules must have `severity: ERROR` to serve as hard blocking gates.
2. **Paired Test Fixtures**: Every rule YAML file (`*.yaml`) must have a corresponding test fixture (`.py`, `.cs`, or `.sh`) containing:
   - At least one positive trigger case marked with `# ruleid: <rule-id>` or `// ruleid: <rule-id>`.
   - At least one negative false-positive guard marked with `# ok: <rule-id>` or `// ok: <rule-id>`.
   - **Whole-file-scope rules** (e.g. "the file must start with a shebang", "the file must set `-e` somewhere") check a single fact about the entire file, so a positive and a negative case cannot coexist in one fixture. For these, put the positive case in `<rule-id>.sh` and the negative case alone in `<rule-id>.ok.sh`; the test suite uses the `.ok.<ext>` file for the negative check when it exists. Every rule of this shape MUST be regex-anchored to the whole file (e.g. `\A(?!#!)` for "must start with X", `(?s)\A.*\Z` paired with `pattern-not-regex` for "must contain X somewhere") — never gated behind an unrelated token that happens to appear in the fixture, which lets the rule pass tests while detecting nothing on real code.
3. **Quoting Special Syntax**: In YAML, all pattern strings containing colons, curly braces `{}`, brackets `[]`, or quotes must be quoted to prevent parser errors.
4. **Mandatory Test Verification**:
   Before committing or finalizing changes, execute the test suite:
   ```bash
   pytest
   ```
   Both the Python and C# rule test suites (including schema checks, positive detections, and false-positive guards) must pass with a 100% success rate.

---

## 📦 Consuming the Packages

### 🐍 Python (`thruput-semgrep-rules`)

1. **Add Dependency**:
   ```toml
   [project.optional-dependencies]
   dev = [
       "thruput-semgrep-rules @ git+https://github.com/thruput/semgrep.git#subdirectory=python"
   ]
   ```
2. **Run Linter**:
   ```bash
   thruput-semgrep .
   # or
   semgrep-python .
   ```
3. **Programmatic Access**:
   ```python
   from semgrep_rules import get_rules_path

   rules_dir = get_rules_path()
   ```

---

### ⚡ .NET (`Thruput.Semgrep.Rules`)

The .NET package includes an auto-bootstrapping mechanism that automatically downloads the standalone Semgrep binary on first execution if not already installed.

1. **Add NuGet Package**:
   ```bash
   dotnet add package Thruput.Semgrep.Rules
   ```
2. **Run Linter via MSBuild Target**:
   ```bash
   dotnet build -t:ThruputSemgrepLint
   ```
3. **Enable Automatic Scan on Every Build (Optional)**:
   Add to `.csproj` or `Directory.Build.props`:
   ```xml
   <PropertyGroup>
     <EnableThruputSemgrepOnBuild>true</EnableThruputSemgrepOnBuild>
   </PropertyGroup>
   ```
