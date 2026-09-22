#!/bin/bash
set -euo pipefail

# ok: no-disabling-via-pragma
# shellcheck shell=bash

# ruleid: no-disabling-via-pragma
# shellcheck disable=SC2086
rm -rf $DIR
