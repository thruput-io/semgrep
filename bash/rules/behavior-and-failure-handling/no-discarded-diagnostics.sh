#!/bin/bash
set -euo pipefail

# ok: no-discarded-diagnostics
ls -la /tmp > /tmp/output.log

# ruleid: no-discarded-diagnostics
ls -la /tmp 2> /dev/null

# ruleid: no-discarded-diagnostics
ls -la /tmp > /dev/null 2>&1

# ruleid: no-discarded-diagnostics
ls -la /tmp &> /dev/null

# ruleid: no-discarded-diagnostics
curl -s https://example.com 2>>/dev/null
