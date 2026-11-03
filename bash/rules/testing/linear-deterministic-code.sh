#!/usr/bin/env bash

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

# ok: linear-deterministic-code
@test "passes here-string input to command" {
  run get_config <<< "for each item in input until case while if"
  [ "$status" -eq 0 ]
}

# ok: linear-deterministic-code
test_linear_shell_helper() {
  actual=$(get_config "host")
  [ "$actual" = "localhost" ]
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
@test "loops with while" {
  while read -r line; do
    run process "$line"
  done < input.txt
}

# ruleid: linear-deterministic-code
@test "loops with until" {
  until check_ready; do
    sleep 1
  done
}

# ruleid: linear-deterministic-code
@test "branches with case" {
  run detect_os
  case "$output" in
    linux) [ "$status" -eq 0 ] ;;
  esac
}

# ruleid: linear-deterministic-code
test_wrapped_branch_in_function() {
  { if [ "$1" = "linux" ]; then echo "ok"; fi; }
}

# ruleid: linear-deterministic-code
for pkg in alpha beta; do
  run_check "$pkg"
done

# ruleid: linear-deterministic-code
until check_service_up; do
  sleep 1
done
