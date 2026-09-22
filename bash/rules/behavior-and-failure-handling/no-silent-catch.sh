#!/bin/bash
set -euo pipefail

# ok: no-silent-catch
trap 'echo "cleanup"; exit 1' ERR

# ok: no-silent-catch
trap cleanup_fn EXIT

# ruleid: no-silent-catch
trap '' ERR

# ruleid: no-silent-catch
trap "" EXIT
