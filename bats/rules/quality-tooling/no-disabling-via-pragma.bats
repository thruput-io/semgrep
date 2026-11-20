#!/usr/bin/env bats

@test "disables shellcheck" {
  # ruleid: no-disabling-via-pragma
  # shellcheck disable=SC2086
  echo $UNQUOTED
}

@test "clean test" {
  # ok: no-disabling-via-pragma
  echo "${QUOTED}"
}
