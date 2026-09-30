# Reboot and recovery

The linuwu-sense-an51545-dkms Arch package installs source under /usr/src.
Arch's installed DKMS pacman hooks rebuild for kernel/header updates. Keep the
matching kernel headers and compiler packages installed. A future kernel can
still introduce an incompatible API: inspect DKMS output after upgrades.

nitrosense-driver.service runs before nitrosense-daemon.service. It checks the
model and availability of a module for the running kernel, replaces acer_wmi
if necessary, and requests automatic fan mode. A failed module load or fan
initialization attempts to restore acer_wmi. Neither a stock-driver blacklist
nor forced model parameters is installed. A known-good LTS kernel remains.

The daemon is enabled at boot. The GUI opens from the KDE menu on demand; it
is not opened automatically. Fans initialize to auto. No saved lighting, CPU
mode or fan duty is restored by the Python service. Firmware/driver persistence
for the charge limit and keyboard lighting needs an actual reboot check.
Current settings before reboot are in evidence/pre-reboot-settings.json.

## After the next reboot

Open NitroSense Linux and check that it connects. Inspect DKMS status and both
services, confirm fans are in Automatic, and compare charge limit and keyboard
lighting against the saved pre-reboot state. Then test suspend/resume while
idle. Do not call reboot/suspend validation complete until those are observed.

## Restore stock behavior

Run:

    sudo /usr/local/lib/nitrosense/restore-stock-driver.sh

This disables both NitroSense services, restores auto fan mode, unloads the
custom driver, and loads acer_wmi. If the system cannot reach the desktop,
boot the installed LTS kernel or add these temporary kernel command-line flags
in the bootloader editor:

    module_blacklist=linuwu_sense systemd.mask=nitrosense-driver.service systemd.mask=nitrosense-daemon.service

Then disable the two services and remove the DKMS package if desired:

    sudo systemctl disable nitrosense-driver.service nitrosense-daemon.service
    sudo pacman -R linuwu-sense-an51545-dkms

Never force-unload a busy kernel module. If normal unload fails, boot with the
recovery flags instead. Neither unloading nor reinstalling a driver guarantees
restoration of firmware-persistent battery or lighting settings.
