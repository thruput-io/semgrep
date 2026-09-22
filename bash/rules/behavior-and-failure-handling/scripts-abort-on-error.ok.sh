#!/bin/bash
set -euo pipefail

# ok: scripts-abort-on-error
rm -rf "$TARGET_DIR"
echo "Safe code after set -euo pipefail"
