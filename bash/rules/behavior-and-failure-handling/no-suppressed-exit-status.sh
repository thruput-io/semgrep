#!/bin/bash
set -euo pipefail

# ok: no-suppressed-exit-status
do_something_safely || handle_error

# ruleid: no-suppressed-exit-status
do_something || true

# ruleid: no-suppressed-exit-status
do_something_else || :

# ruleid: no-suppressed-exit-status
grep -q "pattern" /var/log/app.log || true

# ruleid: no-suppressed-exit-status
check_baseline "$1" || return 0

# ruleid: no-suppressed-exit-status
verify_state || exit 0

# ruleid: no-suppressed-exit-status
baseline_exists "$1" || { printf '%s\n' "$committed_version"; return 0; }

# ruleid: no-suppressed-exit-status
baseline_exists "$1" || { printf '%s\n' "$committed_version"; exit 0; }

# ok: no-suppressed-exit-status
check_baseline "$1" || return 1

# ok: no-suppressed-exit-status
verify_state || exit 1

# ok: no-suppressed-exit-status
baseline_exists "$1" || { printf '%s\n' "missing" >&2; return 1; }

# ok: no-suppressed-exit-status
baseline_exists "$1" || { printf '%s\n' "missing" >&2; exit 1; }
