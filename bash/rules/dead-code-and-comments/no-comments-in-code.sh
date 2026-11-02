#!/bin/bash
# shellcheck shell=bash
set -euo pipefail

# ok: no-comments-in-code
echo "No comment on this line"

# ruleid: no-comments-in-code
# This is an illegal comment explaining code

# ok: no-comments-in-code
#DEBHELPER#

# ok: no-comments-in-code
cat <<'EOF'
# Markdown heading inside heredoc
## Subheading inside heredoc
EOF
