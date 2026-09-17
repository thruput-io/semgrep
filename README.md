# Thruput Semgrep Rules (Python & .NET)

Curated, production-grade Semgrep rulesets maintained by **Thruput** for **Python** and **.NET (C#)** codebases, designed to catch subtle bugs, mutable state pitfalls, null safety violations, security vulnerabilities, performance anti-patterns, and framework misuse.

Cleanly separated into two independent packages:
- 🐍 **`python/`**: Python package `thruput-semgrep-rules-python` + `semgrep-python` CLI runner
- ⚡ **`csharp/`**: .NET NuGet package `Thruput.Semgrep.Rules` with **zero-setup auto-bootstrapping CLI** + MSBuild integration
- 🤖 **`.github/`**: GitHub Actions CI/CD workflows for testing, building, and publishing

---

## 📁 Repository Structure

```
.
├── .github/
│   └── workflows/
│       ├── ci.yml                  # GitHub Actions CI matrix (Python & C# test/build)
│       └── publish.yml             # GitHub Actions publishing workflow (PyPI & NuGet)
│
├── python/                         # 🐍 Self-contained Python Package
│   ├── rules/                      # Canonical Python Semgrep rules & test fixtures
│   │   ├── correctness/
│   │   ├── security/
│   │   ├── frameworks/
│   │   └── style/
│   ├── src/
│   │   └── semgrep_rules/          # Python module source
│   │       ├── __init__.py         # get_rules_path() resolution
│   │       ├── cli.py              # semgrep-python CLI entrypoint
│   │       └── py.typed            # PEP 561 marker
│   ├── tests/
│   │   └── test_python_rules.py    # Pytest suite for Python rules & schema validation
│   ├── pyproject.toml              # Python build & dependency config (thruput-semgrep-rules-python)
│   └── pytest.ini                  # Pytest configuration
│
├── csharp/                         # ⚡ Self-contained .NET NuGet Package
│   ├── rules/                      # Canonical C# Semgrep rules & test fixtures
│   │   ├── correctness/
│   │   ├── security/
│   │   ├── performance/
│   │   └── style/
│   ├── build/
│   │   └── Thruput.Semgrep.Rules.targets # MSBuild integration & CLI auto-bootstrapper
│   ├── tests/
│   │   └── test_csharp_rules.py    # Test suite for C# rules & schema validation
│   └── Thruput.Semgrep.Rules.csproj # NuGet package project definition
│
└── README.md
```

---

## 📖 Engineering Playbook: Changes & Quality Invariants

> ### ⚠️ Strict Quality Policy
> **The repository must ALWAYS remain in a fully valid, runnable, and tested state.**
> 
> **ANY change** (adding new rules, editing existing patterns, updating metadata, or modifying fixtures) **STRICTLY REQUIRES all tests to pass with 100% success** before merging. Broken rules, syntax errors, or unverified patterns are not permitted.

### Playbook Checklist for Any Rule Change:
1. **Quote All Patterns**: In YAML, all single-line pattern strings containing syntax characters (`{}`, `[]`, `""`, colons `:`, or string interpolation) **must be quoted** to prevent YAML mapping parse errors.
2. **Include Required Metadata**: Every rule must have:
   - Unique, kebab-case `id` prefixed with language (`python-` or `csharp-`).
   - Clear and actionable `message`.
   - Valid `languages` array.
   - Severity: `ERROR`, `WARNING`, or `INFO`.
   - `metadata.category` (e.g. `correctness`, `security`, `performance`, `frameworks`, `style`).
3. **Provide Test Fixtures**:
   - Every rule YAML file must have a paired fixture (`.py` for Python, `.cs` for C#).
   - Fixtures must include at least one positive `# ruleid: <id>` / `// ruleid: <id>` match.
   - Fixtures must include at least one negative false-positive guard `# ok: <id>` / `// ok: <id>`.
4. **Run and Pass Local Tests**:
   - For Python: `cd python && pytest`
   - For C#: `cd csharp && pytest tests/`
5. **GitHub Actions CI Gate**:
   Pull requests run `.github/workflows/ci.yml` and will be automatically blocked from merging if any test fails.

---

## 📦 Consuming in Other Projects

### 🐍 In Python Projects

#### 1. Add to Dependencies
```toml
# In downstream pyproject.toml
[project.optional-dependencies]
dev = [
    # From PyPI / GitHub Packages
    "thruput-semgrep-rules-python>=0.1.0",
    # Or directly from GitHub
    "thruput-semgrep-rules-python @ git+https://github.com/thruput/semgrep.git#subdirectory=python"
]
```

#### 2. Run via CLI
```bash
# Scan current directory with bundled Python rules
semgrep-python .

# Pass custom semgrep flags
semgrep-python --error --exclude "tests/**" .
```

#### 3. Programmatic Access
```python
from semgrep_rules import get_rules_path

rules_dir = get_rules_path()
```

---

### ⚡ In .NET / C# Projects (Zero-Setup Auto-Bootstrapping)

Your colleagues do **not** need to install Python, Brew, or any CLI beforehand. The NuGet package automatically downloads the standalone Semgrep binary on the first run if not already present on their system.

#### 1. Add NuGet Package
```bash
dotnet add package Thruput.Semgrep.Rules
```
Or in your `.csproj`:
```xml
<ItemGroup>
  <PackageReference Include="Thruput.Semgrep.Rules" Version="0.1.0">
    <PrivateAssets>all</PrivateAssets>
  </PackageReference>
</ItemGroup>
```

#### 2. Run via MSBuild Target
```bash
# Runs Semgrep against project files (auto-bootstrapping CLI if needed)
dotnet build -t:ThruputSemgrepLint
```

#### 3. Enable Automatic Linting on Every Build (Optional)
In your `.csproj` or `Directory.Build.props`:
```xml
<PropertyGroup>
  <EnableThruputSemgrepOnBuild>true</EnableThruputSemgrepOnBuild>
</PropertyGroup>
```

---

## 📋 Rule Catalog

### 🐍 Python Rules (`python/rules/`)

| Rule ID | Severity | Category | Description |
| :--- | :--- | :--- | :--- |
| `python-mutable-default-arg` | **ERROR** | Correctness | Detects mutable default arguments (`[]`, `{}`, `set()`) evaluated at definition time. |
| `python-compare-none-equality` | **WARNING** | Correctness | Flags `== None` or `!= None`; enforces `is None` and `is not None`. |
| `python-dangerous-iteration-mutation` | **ERROR** | Correctness | Catches mutating dictionaries or lists (`del`, `remove`, `pop`) while iterating over them. |
| `python-falsy-empty-string-check` | **WARNING** | Correctness | Flags `str or default` which unintentionally replaces empty strings `""` with defaults. |
| `python-none-attribute-access` | **WARNING** | Correctness | Detects unsafe chained method calls on `.get()` without `None` guards or defaults. |
| `python-assert-tuple-statement` | **ERROR** | Correctness | Detects `assert (cond, msg)` which always evaluates to `True` in Python. |
| `python-no-none-collection-return` | **ERROR** | Correctness | Prevents returning `None` from functions annotated with collection return types (`list`, `dict`, `set`, `Sequence`). |
| `python-no-return-none-without-optional` | **ERROR** | Correctness | Flags returning `None` in functions annotated with concrete non-nullable return types (enforces `Optional[T]` / `T \| None` contracts). |
| `python-in-place-mutation-none-assignment` | **ERROR** | Correctness | Catches assignment of in-place list methods (`x = x.sort()`, `x = x.append(...)`) that overwrite data with `None`. |
| `python-regex-none-dereference` | **ERROR** | Correctness | Flags direct chained `.group()` calls on `re.search` / `re.match` without `None` check. |
| `python-dangerous-eval-exec` | **ERROR** | Security | Catches dynamic `eval()` or `exec()` with variable input. |
| `python-insecure-deserialization` | **ERROR** | Security | Flags insecure deserialization with `pickle` or unloader `yaml.load`. |
| `python-subprocess-shell-true` | **ERROR** | Security | Detects `subprocess` calls with `shell=True` using dynamic strings. |
| `python-sql-string-formatting` | **ERROR** | Security | Flags string interpolation/formatting passed directly into SQL query execution. |
| `python-flask-debug-true` | **ERROR** | Frameworks | Detects `app.run(debug=True)` or `app.config['DEBUG'] = True`. |
| `python-django-raw-sql` | **ERROR** | Frameworks | Flags raw SQL string formatting in Django `raw()` or `extra()`. |
| `python-fastapi-mutable-dependency` | **WARNING** | Frameworks | Flags mutable default arguments in FastAPI path/query operations. |
| `python-bare-except` | **WARNING** | Style | Catches bare `except:` blocks that mask `KeyboardInterrupt` and `SystemExit`. |
| `python-repeated-regex-compile` | **WARNING** | Performance | Detects `re.compile()` invoked inside loops on every iteration. |
| `python-no-comments` | **WARNING** | Style | Flags inline `#` comments (except `# type: ignore`, `# noqa`, `# pragma:`, shebangs). |
| `python-avoid-passing-none-literal` | **WARNING** | Style | Flags passing `None` literals directly into function calls (encourages default arguments). |

---

### ⚡ C# Rules (`csharp/rules/`)

| Rule ID | Severity | Category | Description |
| :--- | :--- | :--- | :--- |
| `csharp-compare-null-equality` | **WARNING** | Correctness | Flags `== null` / `!= null`; recommends pattern matching `is null` / `is not null`. |
| `csharp-dangerous-collection-mutation` | **ERROR** | Correctness | Detects collection modifications (`.Remove()`, `.Add()`) inside `foreach` loops. |
| `csharp-empty-string-comparison` | **WARNING** | Correctness | Flags `s == ""` or `s != ""`; recommends `string.IsNullOrEmpty` / `string.IsNullOrWhiteSpace`. |
| `csharp-unsafe-nullable-value-access` | **WARNING** | Correctness | Flags direct `.Value` access on `Nullable<T>` without `.HasValue` checks. |
| `csharp-avoid-passing-null-literal` | **INFO** | Correctness | Flags passing literal `null` arguments into method invocations. |
| `csharp-ef-core-sql-injection` | **ERROR** | Security | Detects interpolated strings in `FromSqlRaw` / `ExecuteSqlRaw` (use `FromSqlInterpolated`). |
| `csharp-insecure-binary-formatter` | **ERROR** | Security | Detects `BinaryFormatter.Deserialize` (vulnerable to remote code execution). |
| `csharp-weak-hashing-md5-sha1` | **WARNING** | Security | Detects broken cryptographic hash algorithms (`MD5.Create()`, `SHA1.Create()`). |
| `csharp-sync-over-async-deadlock` | **WARNING** | Performance | Flags `.Result`, `.Wait()`, `.GetAwaiter().GetResult()` on asynchronous Tasks. |
| `csharp-httpclient-creation-lifecycle` | **WARNING** | Performance | Flags `new HttpClient()` in methods causing socket exhaustion; recommends `IHttpClientFactory`. |
| `csharp-linq-multiple-enumeration` | **WARNING** | Performance | Flags multiple enumerations of `IEnumerable` (e.g. `if (items.Any()) foreach (...)`). |
| `csharp-empty-catch-block` | **WARNING** | Style | Detects empty `catch` blocks that silently swallow exceptions. |
| `csharp-no-comments` | **WARNING** | Style | Flags `//` and `/* */` comments (except XML doc `///`, `<auto-generated>`, pragmas). |

---

## 🛠️ Local Development & Testing

### Python Workspace
```bash
cd python
pip install -e ".[dev]"
pytest
python -m build
```

### C# Workspace
```bash
cd csharp
dotnet pack Thruput.Semgrep.Rules.csproj -c Release -o dist
```
