#!/usr/bin/env bash
set -euo pipefail
[[ $EUID -eq 0 ]] || { echo 'Administrator access required' >&2; exit 1; }
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
install -d -m 755 /usr/local/lib/nitrosense /etc/nitrosense
install -m 644 "$root/service/nitrosense-daemon.py" "$root/service/PowerSourceDetection.py" "$root/service/control_policy.py" /usr/local/lib/nitrosense/
install -m 600 "$root/packaging/nitrosense-access.conf" /etc/nitrosense/access.conf
install -m 644 "$root/packaging/nitrosense-daemon.service" /etc/systemd/system/nitrosense-daemon.service
systemctl daemon-reload
systemctl restart nitrosense-daemon.service
