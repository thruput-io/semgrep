import functools
import http.server
import os
import subprocess
import threading
from pathlib import Path
import yaml
from scripts.bundle_rules import bundle_all_rulesets

REPO_ROOT = Path(__file__).resolve().parent.parent
JS_BAD_FIXTURE = REPO_ROOT / "javascript" / "rules" / "domain-modeling" / "no-mutators.js"
JS_OK_FIXTURE = REPO_ROOT / "javascript" / "rules" / "quality-tooling" / "max-file-lines.ok.js"


def load_rules_count(path: Path) -> int:
    with open(path, "r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    return len(data["rules"])


def start_static_server(directory: Path) -> tuple[http.server.HTTPServer, int]:
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(directory))
    server = http.server.HTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    return server, server.server_port


def test_bundle_creates_language_and_combined_rulesets(tmp_path: Path) -> None:
    bundle_all_rulesets(REPO_ROOT, tmp_path)
    python_count = load_rules_count(tmp_path / "python.yaml")
    csharp_count = load_rules_count(tmp_path / "csharp.yaml")
    bash_count = load_rules_count(tmp_path / "bash.yaml")
    javascript_count = load_rules_count(tmp_path / "javascript.yaml")
    all_count = load_rules_count(tmp_path / "all.yaml")
    rules_count = load_rules_count(tmp_path / "rules.yaml")
    index_count = load_rules_count(tmp_path / "index.html")
    assert python_count > 0
    assert csharp_count > 0
    assert bash_count == 14
    assert javascript_count == 19
    assert all_count == python_count + csharp_count + bash_count + javascript_count
    assert rules_count == all_count
    assert index_count == all_count


def test_bundled_rulesets_validate_with_semgrep(tmp_path: Path) -> None:
    bundle_all_rulesets(REPO_ROOT, tmp_path)
    res_all = subprocess.run(
        ["semgrep", "scan", "--validate", "--config", str(tmp_path / "all.yaml")],
        capture_output=True,
        text=True,
        check=True,
    )
    res_js = subprocess.run(
        ["semgrep", "scan", "--validate", "--config", str(tmp_path / "javascript.yaml")],
        capture_output=True,
        text=True,
        check=True,
    )
    res_bash = subprocess.run(
        ["semgrep", "scan", "--validate", "--config", str(tmp_path / "bash.yaml")],
        capture_output=True,
        text=True,
        check=True,
    )
    assert res_all.returncode == 0
    assert res_js.returncode == 0
    assert res_bash.returncode == 0


def test_semgrep_config_url_scans_via_http(tmp_path: Path) -> None:
    bundle_all_rulesets(REPO_ROOT, tmp_path)
    server, port = start_static_server(tmp_path)
    clean_env = {k: v for k, v in os.environ.items() if k != "SEMGREP_RULES"}
    bad_scan = subprocess.run(
        [
            "semgrep",
            "--error",
            "--config",
            f"http://127.0.0.1:{port}/javascript.yaml",
            str(JS_BAD_FIXTURE),
        ],
        capture_output=True,
        text=True,
        env=clean_env,
        check=False,
    )
    ok_scan = subprocess.run(
        [
            "semgrep",
            "--error",
            "--config",
            f"http://127.0.0.1:{port}/javascript.yaml",
            str(JS_OK_FIXTURE),
        ],
        capture_output=True,
        text=True,
        env=clean_env,
        check=True,
    )
    server.shutdown()
    assert bad_scan.returncode != 0
    assert ok_scan.returncode == 0
