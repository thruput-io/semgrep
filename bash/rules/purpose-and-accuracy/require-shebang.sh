# ruleid: require-shebang
set -euo pipefail
echo "This file has no shebang at all, so the whole file violates the rule"
echo "any real command shape below must still be caught"
grep -q "pattern" /var/log/app.log
