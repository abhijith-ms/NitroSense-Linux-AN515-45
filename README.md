# Acer Nitro controls for CachyOS

Experimental integration project for Acer Nitro AN515-45. Project location:
`/home/abhijithms/Documents/acer-nitro-controls`.
Independent repository; no changes to aura-store.

## Graphical app and startup integration

Open **NitroSense Linux** in the KDE application menu, or run
`scripts/launch-ui.sh` from this project.

- Performance: automatic/manual CPU and GPU fans and Linux CPU power modes.
- Battery: **80% charge limit**, USB charging and calibration (explicit confirmation).
- Keyboard: four-zone colors, brightness, effects and idle timeout.
- Monitoring: live temperatures, fan RPM and utilization.

The daemon is installed at /usr/local/lib/nitrosense and running as
nitrosense-daemon.service. Its socket is restricted to the configured account
using filesystem permissions and peer credentials. Startup does not restore
saved settings, reload drivers or change power profiles. The GUI is unprivileged.
Driver-forcing controls and the GNOME shortcut prompt are removed from this build.
For a KDE shortcut, assign the NitroSense Linux launcher in System Settings.

The driver is installed through the local Arch package
linuwu-sense-an51545-dkms. DKMS installation passed for both 7.2.8-1-cachyos
and 6.18.52-1-cachyos-lts. Arch DKMS hooks rebuild on kernel/header updates.
The driver and daemon services are enabled at boot. Fans initialize to firmware
auto; automatic saved lighting/CPU/fan restores remain disabled in the daemon.
The GUI opens on demand from the KDE menu. Closing it does not reset a manual
fan selection; select Automatic first if desired.

See docs/reboot-and-recovery.md for the recovery script and bootloader recovery
flags. No stock-driver blacklist was installed. A real reboot and suspend/resume
validation remain pending. The user reported the UI and controls working before
this persistence setup; charge cutoff at 80% still needs observation.

Verified: UI production build and typecheck, seven upstream test suites, four
local policy/startup tests, live read-only service connection, rejected invalid
requests, and a screenshot of the connected Battery screen. No valid hardware
write was performed during UI integration. Battery cutoff near 80%, visible RGB
and fan command behavior still need interactive verification on BIOS V1.11.
Production npm dependencies audit clean; build dependencies retain upstream
audit findings (see work/npm-audit.json). This is a local development build.

## Initial investigation — 2026-09-30

Read-only checks confirmed Nitro AN515-45, BIOS V1.11, CachyOS running
7.2.6-1-cachyos. Installed kernel/header pairs are 7.2.8-1-cachyos and
6.18.52-1-cachyos-lts; headers for the running kernel are absent. Secure Boot
variable was 0; lockdown reports none. Stock acer_wmi is loaded. No Linuwu
feature nodes, charge-control threshold attributes, or keyboard LED device
were exposed. Absence of those nodes does not establish lack of hardware support.
CPU/GPU, RAM and desktop versions were supplied by the user's screenshot.

All three NitroSense driver patches apply to Div-Linuwu-Sense at the pinned
revision. They do NOT apply to the original Linuwu-Sense revision reviewed.
Both drivers initially failed against 7.2.8 on obsolete strncpy calls.
Our additional patch replaces three bounded copies with memcpy, retaining the
existing termination and adding zero-length guards before len-1 indexing.
The patched fork compiled successfully against both installed kernel/header
pairs. Two upstream boolean bitwise-AND warnings remain in the Clang build.
Compilation is not proof of BIOS V1.11 compatibility or safe runtime behavior.
No driver was installed, signed, loaded, or activated. No settings were changed.

## Contents

- `upstream.lock.json`: exact revisions and source URLs.
- `packaging/linuwu-sense-an51545-dkms/`: experimental PKGBUILD, DKMS configuration,
  build helper and four patches. No auto-load or blacklist configuration.
- `scripts/check-hardware.py`: read-only inventory without serial numbers.
- `evidence/`: inventory and successful compiler logs.
- `docs/approach.md`: packaging, desktop integration and activation gates.
- `work/upstream/`: local source checkouts (ignored by Git).

Run `python scripts/check-hardware.py` to repeat the read-only inventory.
Package installation and hardware activation are deliberately deferred.
The PKGBUILD has passed shell syntax checks; makepkg/DKMS installation and GUI
build/testing have not yet been performed. Build logs are from direct Kbuild.

## Upstreams

[NitroSense Linux AN515-45](https://github.com/MeetSolanki530/NitroSense-Linux-AN515-45)
provides an Electron/React app and Python daemon. Its reported test system uses
BIOS V1.14, Ryzen 7 5800H, RTX 3050 Ti and Zorin/GNOME. That is not validation
of this machine's BIOS V1.11 or KDE session.

[Linuwu-Sense](https://github.com/0x7375646F/Linuwu-Sense) is the original driver.
NitroSense's BUILDING.md points there, but its patches/README.md names
[Div-Linuwu-Sense](https://github.com/PXDiv/Div-Linuwu-Sense), which matches the
patches in practice. Three patches are needed, not just the two listed in
BUILDING.md.

[OpenSense](https://github.com/archivesteak/opensense) is a Windows .NET 10 /
Windows App SDK project. Use it as a behavior/protocol reference, not a Linux
application to package directly.

## License review

NitroSense's LICENSE assigns MIT to app/packaging, GPL-3.0 to the Python service,
and GPL-2.0 to driver patches. Driver source declares GPL-2.0-or-later, while
its repository LICENSE contains GPLv3. Preserve all notices and clarify this
metadata mismatch before public redistribution. The draft package metadata
follows the source SPDX provisionally. OpenSense has GPLv3; copying its code
requires a separate license review. No OpenSense code is included here.
The local kernel-string-copy patch follows the driver's GPL-2.0-or-later notice.
