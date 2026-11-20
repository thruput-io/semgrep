#!/usr/bin/env bats

# ok: no-muted-tests
@test "addition works" {
  result="$(echo 2+2 | bc)"
  [ "$result" -eq 4 ]
}

# ruleid: no-muted-tests
@test "not ready yet" {
  skip "flaky in CI"
  false
}
