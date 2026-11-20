#!/usr/bin/env bats

@test "default on failure" {
  # ruleid: no-default-on-failure
  val="${MISSING_VAR:-fallback}"
  # ruleid: no-default-on-failure
  out="$(failing_cmd || echo default)"
  # ruleid: no-default-on-failure
  res=$(other_cmd) || res="none"
}

@test "fail fast on missing" {
  # ok: no-default-on-failure
  val="${REQUIRED_VAR}"
  # ok: no-default-on-failure
  run get_value
  [ "$status" -eq 0 ]
}
