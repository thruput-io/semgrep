#!/usr/bin/env bats

@test "branching in test" {
  # ruleid: linear-deterministic-code
  if [ "$ENV" = "ci" ]; then
    echo "ci"
  fi

  # ruleid: linear-deterministic-code
  for item in a b c; do
    echo "$item"
  done

  # ruleid: linear-deterministic-code
  while false; do
    echo "loop"
  done

  # ruleid: linear-deterministic-code
  case "$MODE" in
    fast) echo "fast" ;;
  esac
}

@test "linear deterministic test" {
  # ok: linear-deterministic-code
  run my_command arg1
  [ "$status" -eq 0 ]
  [ "$output" = "expected" ]
}
