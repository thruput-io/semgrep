# shellcheck shell=bash
# ok: require-shebang
set -euo pipefail

sourced_helper() {
  echo "A file under lib/ is sourced, never run, so it carries no shebang"
}
