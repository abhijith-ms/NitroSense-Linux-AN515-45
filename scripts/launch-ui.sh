#!/usr/bin/env bash
set -euo pipefail
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
unset ELECTRON_RUN_AS_NODE ELECTRON_NO_ATTACH_CONSOLE
exec "$root/app/node_modules/electron/dist/electron" "$root/app" "$@"
