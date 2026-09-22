#!/bin/bash
set -euo pipefail

# ok: require-shebang
echo "This file starts with a valid shebang, so nothing should be flagged"
grep -q "pattern" /var/log/app.log
