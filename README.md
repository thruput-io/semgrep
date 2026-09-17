# Thruput Semgrep Rules

Curated Semgrep rulesets for **Python** and **.NET (C#)** codebases.

---

## 🔄 Development & Verification Workflow

> ### ⚠️ Mandatory Invariant
> **Every single modification must be verified before work is considered complete.**
>
> Never assume a rule pattern or change works without running the test suite. Breaking changes, syntax errors, or unverified patterns are not allowed.

### Rule Modification Requirements:
1. **Paired Test Fixtures**: Every rule YAML file (`*.yaml`) must have a corresponding test fixture (`.py` or `.cs`) containing:
   - At least one positive trigger case marked with `# ruleid: <rule-id>` or `// ruleid: <rule-id>`.
   - At least one negative false-positive guard marked with `# ok: <rule-id>` or `// ok: <rule-id>`.
2. **Quoting Special Syntax**: In YAML, all pattern strings containing colons, curly braces `{}`, brackets `[]`, or quotes must be quoted to prevent parser errors.
3. **Mandatory Test Verification**:
   Before committing or finalizing changes, execute the test suite:
   ```bash
   pytest
   ```
   Both the Python and C# rule test suites (including schema checks, positive detections, and false-positive guards) must pass with a 100% success rate.

---

## 📦 Consuming the Packages

### 🐍 Python (`thruput-semgrep-rules-python`)

1. **Add Dependency**:
   ```toml
   [project.optional-dependencies]
   dev = [
       "thruput-semgrep-rules-python @ git+https://github.com/thruput/semgrep.git#subdirectory=python"
   ]
   ```
2. **Run Linter**:
   ```bash
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
