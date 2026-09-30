# Integration and validation plan

## Arch/CachyOS packaging

Build separate packages for the DKMS module, privileged Python daemon and
unprivileged Electron app. Do not convert the Debian package or run its
post-install script: it blacklists/reloads drivers, starts services, and sets
Electron's sandbox permissions. Do not run upstream make install. Even its
plain make target can call sudo for signing; our helper invokes Kbuild directly.

The draft DKMS package pins Div-Linuwu-Sense and carries checksummed patches.
Source lands in /usr/src/linuwu-sense-an51545-0.2.0.r1. DKMS uses its target
kernel version, not uname, and the helper selects LLVM for Clang kernel configs.
Arch's DKMS hooks should rebuild after kernel/header changes. Validate those
hooks in a disposable environment before deployment, including a failed build
and rollback. Both matching CachyOS headers and the kernel's compiler toolchain
must remain installed. DKMS signing must be configured separately if Secure
Boot is later enabled; do not disable Secure Boot as a packaging workaround.

Next packaging checks: clean makepkg build, namcap, unpacked file/permission
inspection, disposable-root DKMS build, and kernel-update rebuild test. Never
ship the stock-driver blacklist or module autoload before hardware validation.
The PKGBUILD is a scaffold, not a tested release package.

For the app, use the pinned npm lockfile with npm ci in an isolated build tree;
review lifecycle scripts first. Build Electron and Vite outputs, retain the
Electron sandbox, and stage a desktop file and icons. Prefer a validated Arch
Electron runtime or explicitly package/audit the bundled runtime. Upstream uses
Electron 44, React 19, Vite 8, TypeScript 7 and electron-builder 26; its local
Node 22 compatibility must be checked against the locked tool engine ranges.
Run typecheck and seven offline test scripts. Do not run test:e2e: it writes to
real hardware. Remove Debian-specific auto-start/install logic and bundled
driver resources from the GUI package; use the separate DKMS package instead.

## Daemon boundary

Upstream uses /var/run/nitrosense.sock with mode 0666. Before activation, replace
this with an explicitly authorized control channel: for example root-owned
/run/nitrosense with a dedicated group and 0660 socket plus validated peer
credentials, or a polkit-authorized D-Bus service. A systemd UMask alone cannot
undo an explicit chmod(0666). Test rejection of unauthorized users and invalid
values without hardware. Keep sysfs root-owned; never grant all users writes.

Startup restores saved lighting, fan and CPU mode. Add a monitor-only mode that
does not restore or write settings and use it for initial integration. Validate
fan auto-recovery on daemon crash, application exit and suspend/resume before
allowing persistent manual fan control. Do not assume stopping the daemon
restores firmware fan control. Review driver probe too: the RGB patch issues
keyboard-enable WMI calls during probe, so merely loading it is a hardware change.

Use a system service installed under /usr/lib/systemd/system, disabled by default.
Define state/runtime directories and narrow permissions. Add hardening only
after enumerating the required sysfs paths; ProtectKernelTunables can prevent
intended sysfs writes. Keep CPU governor changes outside the initial scope to
avoid conflicts with KDE's power profile service.

## KDE Plasma X11

Install a normal desktop launcher; run the GUI as the logged-in user. Skip the
GNOME gsettings shortcut helper. In Plasma System Settings > Keyboard >
Shortcuts, assign an application launch shortcut after observing the actual
NitroSense key event (xev can help on X11). Do not guess a keycode or install a
hwdb override before observing it. Test launcher, polkit prompt, single-instance
behavior, scaling and window activation. Autostart stays optional and off during
validation. Fn brightness keys may change physical brightness without accurate
firmware readback, so label app brightness as last requested if appropriate.

## Feature validation, after explicit activation authorization

First boot into a kernel with matching headers and a successful build; preserve
a known-good stock-driver boot path. Never load a 7.2.8 module into running
7.2.6. Plan a temporary stock acer_wmi replacement and rollback before testing;
the two drivers share the platform device. Do not force enable_all or nitro_v4:
the model-specific DMI entry must select behavior. Do not update BIOS merely
to match upstream's test machine.

1. Baseline: record idle temperatures, available sensors, current fan behavior,
   battery status and keyboard appearance. Verify stock keyboard, Wi-Fi/rfkill
   and suspend behavior so driver replacement regressions are detectable.
2. Temporary driver load: capture kernel logs and feature nodes. Driver probe
   itself writes lighting WMI calls. Stop on ACPI errors or regressions; restore
   the stock-driver boot path. No boot persistence yet.
3. Fans: confirm auto mode first, then brief conservative increases only while
   observing both RPM and temperatures. Avoid minimum/zero-duty experiments.
   Return to auto and verify actual behavior. Test failure/recovery paths before
   sustained manual mode or workload testing.
4. Battery: read current limiter state, enable the 80% flag, and observe actual
   charge cessation near 80% from below the threshold. A successful sysfs write
   alone does not pass. If already above 80%, limiting need not discharge it.
   Test AC reconnection, reboot and disable/restore; do not run calibration.
5. Keyboard: confirm this unit's actual four-zone hardware, test low-brightness
   static colors per zone, brightness, then effects. Verify visibly, not just
   readback. Exercise Fn keys, timeout, suspend and reboot. Record restoration
   behavior and a rollback procedure before saving persistent settings.
6. Integration: test KDE launcher/shortcut and restricted daemon access. Only
   enable module/service persistence after each requested feature has a recorded
   pass on BIOS V1.11. Mark unsupported features unavailable, not successful.

Acceptance remains pending for all three requested hardware features. Successful
compilation is the only driver compatibility milestone completed so far.
