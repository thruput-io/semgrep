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
