#!/usr/bin/env bats
set -euo pipefail

# ok: scripts-abort-on-error
@test "has set -euo pipefail" {
  run echo "hello"
  [ "$status" -eq 0 ]
}
