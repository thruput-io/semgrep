# ruleid: require-shebang
@test "missing bats shebang" {
  run echo "hello"
  [ "$status" -eq 0 ]
}
