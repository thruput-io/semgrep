#!/usr/bin/env bats

@test "discards stderr" {
  # ruleid: no-discarded-diagnostics
  run my_cmd 2>/dev/null
  # ruleid: no-discarded-diagnostics
  my_cmd >/dev/null 2>&1
}

@test "preserves stderr" {
  # ok: no-discarded-diagnostics
  run my_cmd
  [ "$status" -eq 0 ]
}
