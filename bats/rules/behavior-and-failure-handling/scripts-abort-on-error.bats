# ruleid: scripts-abort-on-error
#!/usr/bin/env bats

@test "missing set -e" {
  run echo "hello"
  [ "$status" -eq 0 ]
}
