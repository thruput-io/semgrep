#!/usr/bin/env bats

@test "silences trap" {
  # ruleid: no-silent-catch
  trap '' ERR
  # ruleid: no-silent-catch
  trap "" EXIT
}

@test "handles trap" {
  # ok: no-silent-catch
  trap 'echo failed >&2' ERR
}
