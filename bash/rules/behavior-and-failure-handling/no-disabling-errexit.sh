#!/bin/bash
set -euo pipefail

# ok: no-disabling-errexit
set -o pipefail

# ok: no-disabling-errexit
set -o errexit

# ok: no-disabling-errexit
set +u

# ruleid: no-disabling-errexit
set +e

# ruleid: no-disabling-errexit
set +o errexit

# ruleid: no-disabling-errexit
run_unchecked() { set +e; }

# ruleid: no-disabling-errexit
disable_errexit_long() { set +o errexit; }
