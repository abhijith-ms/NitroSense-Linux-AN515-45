#!/usr/bin/env python3
"""Read-only inventory. Does not import upstream code or read serial numbers."""
import json, platform
from pathlib import Path

def read(path):
    try:
        return Path(path).read_text().strip()
    except OSError:
        return None

kernel = platform.release()
root = Path('/sys/devices/platform/acer-wmi')
print(json.dumps({
    'model': read('/sys/class/dmi/id/product_name'),
    'bios': read('/sys/class/dmi/id/bios_version'),
    'running_kernel': kernel,
    'running_kernel_headers': Path('/usr/lib/modules', kernel, 'build/Makefile').exists(),
    'installed_module_trees': sorted(p.name for p in Path('/usr/lib/modules').iterdir()),
    'acer_wmi_nodes': sorted(p.name for p in root.iterdir()) if root.exists() else [],
    'charge_threshold_paths': sorted(str(p) for p in Path('/sys/class/power_supply').glob('*/charge_control*')),
    'leds': sorted(p.name for p in Path('/sys/class/leds').iterdir()),
}, indent=2))
