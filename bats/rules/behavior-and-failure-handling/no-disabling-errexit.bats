#!/usr/bin/env bats

@test "disables errexit" {
  # ruleid: no-disabling-errexit
  set +e
  # ruleid: no-disabling-errexit
  set +o errexit
}

@test "keeps errexit enabled" {
  # ok: no-disabling-errexit
  set -euo pipefail
  run true
  [ "$status" -eq 0 ]
}
