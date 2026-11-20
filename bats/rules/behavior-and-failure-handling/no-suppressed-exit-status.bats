#!/usr/bin/env bats

@test "suppresses exit status" {
  # ruleid: no-suppressed-exit-status
  failing_cmd || true
  # ruleid: no-suppressed-exit-status
  failing_cmd || :
  # ruleid: no-suppressed-exit-status
  failing_cmd || return 0
}

@test "lets failure propagate" {
  # ok: no-suppressed-exit-status
  run ! failing_cmd
  [ "$status" -ne 0 ]
}
