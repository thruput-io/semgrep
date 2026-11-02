#!/bin/bash
set -euo pipefail

# ok: no-default-on-failure
VALUE=$(compute_value)

# ok: no-default-on-failure
cmd || exit 1

# ok: no-default-on-failure
REQUIRED_FEED="${PACKAGE_FEED:?PACKAGE_FEED must be set}"

# ruleid: no-default-on-failure
CONFIG=$(cat file.conf) || CONFIG="default"

# ruleid: no-default-on-failure
PORT=$(get_port 2>/dev/null || echo 8080)

# ruleid: no-default-on-failure
BASELINE=$(git show "origin/main:version.txt" || printf '0.0.0\n')

# ruleid: no-default-on-failure
FEED_NAME="${PACKAGE_FEED:-default-feed}"

# ruleid: no-default-on-failure
BRANCH="${BUILD_SOURCEBRANCHNAME:-$(current_branch)}"

# ruleid: no-default-on-failure
BASE_REF="${1:-origin/main}"

# ruleid: no-default-on-failure
: "${CACHE_DIR:=/tmp/cache}"
