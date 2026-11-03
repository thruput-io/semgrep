#!/bin/bash
set -euo pipefail

# ok: no-silent-catch
trap 'echo "cleanup"; exit 1' ERR

# ok: no-silent-catch
trap "echo cleanup; exit 1" EXIT

# ok: no-silent-catch
trap cleanup_fn EXIT

# ruleid: no-silent-catch
trap '' ERR

# ruleid: no-silent-catch
trap "" EXIT

# ruleid: no-silent-catch
run_step() { trap '' ERR; }

# ruleid: no-silent-catch
clear_exit_trap() { trap "" EXIT; }
