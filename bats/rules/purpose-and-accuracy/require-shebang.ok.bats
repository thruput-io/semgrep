#!/usr/bin/env bats

# ok: require-shebang
@test "has bats shebang" {
  run echo "hello"
  [ "$status" -eq 0 ]
}
