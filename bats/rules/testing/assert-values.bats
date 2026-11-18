#!/usr/bin/env bats

# ok: assert-values
@test "checks the status" {
  run get_config "${some_key}"
  [ "$status" -eq 0 ]
}

# ok: assert-values
@test "checks the output" {
  run list_items
  [ "$output" = "expected" ]
}

# ruleid: assert-values
@test "runs but never checks anything" {
  run do_something
  echo "done"
}

# ruleid: assert-values
@test "runs twice, checks neither" {
  run step_one
  run step_two
}
