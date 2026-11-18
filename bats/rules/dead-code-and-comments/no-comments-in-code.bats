#!/usr/bin/env bats

# ok: no-comments-in-code
# bats file_tags=smoke

# ok: no-comments-in-code
# bats test_tags=fast
@test "tagged test" {
  run echo "ok"
  [ "$status" -eq 0 ]
}

# ok: no-comments-in-code
function bash_syntax_test { #@test
  run echo "ok"
  [ "$status" -eq 0 ]
}

@test "commented test" {
  # ruleid: no-comments-in-code
  # This explains why we run echo
  run echo "bad"
  [ "$status" -eq 0 ]
}
