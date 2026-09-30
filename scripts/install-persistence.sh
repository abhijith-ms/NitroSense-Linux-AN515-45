#!/usr/bin/env bash
set -euo pipefail
[[ $EUID -eq 0 ]] || exit 1
root=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)
pkg="$root/packaging/linuwu-sense-an51545-dkms/linuwu-sense-an51545-dkms-0.2.0.r1-1-x86_64.pkg.tar.zst"
[[ -f $pkg ]] || { echo 'Build the DKMS package first' >&2; exit 1; }
pacman -U --noconfirm "$pkg"
for kernel in 7.2.8-1-cachyos 6.18.52-1-cachyos-lts; do
  dkms install -m linuwu-sense-an51545 -v 0.2.0.r1 -k "$kernel"
  modinfo -k "$kernel" linuwu_sense
 done
install -m755 "$root/scripts/activate-driver.sh" "$root/scripts/restore-stock-driver.sh" /usr/local/lib/nitrosense/
install -m644 "$root/packaging/nitrosense-driver.service" "$root/packaging/nitrosense-daemon.service" /etc/systemd/system/
systemctl daemon-reload
systemctl start nitrosense-driver.service
systemctl restart nitrosense-daemon.service
systemctl enable nitrosense-driver.service nitrosense-daemon.service
