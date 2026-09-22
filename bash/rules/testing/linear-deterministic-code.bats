#!/usr/bin/env bats

# ok: linear-deterministic-code
@test "checks a config value" {
  run get_config "${some_key}"
  [ "$status" -eq 0 ]
}

# ruleid: linear-deterministic-code
@test "branches on platform" {
  run detect_os
  if [ "$status" -eq 0 ]; then
    [ "$output" = "linux" ]
  fi
}

# ruleid: linear-deterministic-code
@test "loops over items" {
  for item in a b c; do
    run process "$item"
  done
}
