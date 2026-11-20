#!/usr/bin/env bats

# ok: max-file-lines
@test "short file" {
  run echo "ok"
  [ "$status" -eq 0 ]
}
