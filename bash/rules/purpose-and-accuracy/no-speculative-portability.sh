#!/bin/bash
set -euo pipefail

# ok: no-speculative-portability
command -v docker >/dev/null

# ruleid: no-speculative-portability
if [[ "$OSTYPE" == "darwin"* ]]; then
  echo "mac"
fi

# ruleid: no-speculative-portability
if [ "$(uname -s)" = "Linux" ]; then
  echo "linux"
fi

# ruleid: no-speculative-portability
case "$(uname)" in
  Darwin) echo mac ;;
esac
