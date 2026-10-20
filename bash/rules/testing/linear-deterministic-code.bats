#!/usr/bin/env bats

# ok: linear-deterministic-code
@test "checks a config value" {
  run get_config "${some_key}"
  [ "$status" -eq 0 ]
}

# ok: linear-deterministic-code
@test "assertion message contains word for in double quotes" {
  run get_config "missing"
  [ "$status" -eq 1 ]
  [ "$output" = "no value for the field of that name" ]
}

# ok: linear-deterministic-code
@test "assertion message contains word for in single quotes" {
  run get_config "github"
  [ "$status" -eq 1 ]
  [ "$output" = 'nothing is registered for github/...' ]
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

# ruleid: linear-deterministic-code
@test "branches with real if statement" {
  run echo "checking for updates"
  if [ "$status" -eq 0 ]; then
    [ "$output" = "ok" ]
  fi
}
