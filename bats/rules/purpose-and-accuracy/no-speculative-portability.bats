#!/usr/bin/env bats

# ruleid: no-speculative-portability
@test "checks OSTYPE" {
  if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "mac"
  fi
}

# ruleid: no-speculative-portability
@test "checks uname" {
  if [[ "$(uname -s)" == "Linux" ]]; then
    echo "linux"
  fi
}

# ok: no-speculative-portability
@test "targets designated runtime directly" {
  run echo "linux"
  [ "$status" -eq 0 ]
  [ "$output" = "linux" ]
}
