#!/bin/bash
set -euo pipefail

# ok: no-default-on-failure
VALUE=$(compute_value)

# ok: no-default-on-failure
cmd || exit 1

# ruleid: no-default-on-failure
CONFIG=$(cat file.conf) || CONFIG="default"

# ruleid: no-default-on-failure
PORT=$(get_port 2>/dev/null || echo 8080)
