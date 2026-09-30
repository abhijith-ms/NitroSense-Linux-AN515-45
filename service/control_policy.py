"""Validate the privileged protocol independently of the Electron renderer."""
import re

def peer_allowed(uid, owner):
    return uid in (0, owner)

def validate_command(command, params):
    if not isinstance(command, str) or not isinstance(params, dict):
        raise ValueError("Invalid command envelope")
    reads = {"get_all_settings", "get_thermal_profile", "get_supported_features", "get_version", "get_modprobe_parameter"}
    toggles = {"set_backlight_timeout", "set_battery_calibration", "set_battery_limiter", "set_boot_animation_sound", "set_lcd_override"}
    def integer(key, lo, hi):
        value = params.get(key)
        if type(value) is not int or not lo <= value <= hi:
            raise ValueError(f"{key} must be an integer from {lo} to {hi}")
    if command in reads:
        return
    if command in toggles:
        if type(params.get("enabled")) is not bool:
            raise ValueError("enabled must be a boolean")
    elif command == "set_fan_speed":
        integer("cpu", 0, 100)
        integer("gpu", 0, 100)
    elif command == "set_usb_charging":
        if type(params.get("level")) is not int or params["level"] not in (0, 10, 20, 30):
            raise ValueError("Invalid USB charging level")
    elif command == "set_per_zone_mode":
        integer("brightness", 0, 100)
        for key in ("zone1", "zone2", "zone3", "zone4"):
            if not isinstance(params.get(key), str) or not re.fullmatch(r"[a-fA-F0-9]{6}", params[key]):
                raise ValueError("Invalid zone color")
    elif command == "set_four_zone_mode":
        for key, lo, hi in (("mode",0,7),("speed",0,9),("brightness",0,100),("direction",1,2),("red",0,255),("green",0,255),("blue",0,255)):
            integer(key, lo, hi)
    elif command == "remember_power_mode":
        if params.get("mode") not in ("quiet", "balanced", "performance"):
            raise ValueError("Invalid power mode")
    elif command == "set_thermal_profile":
        if params.get("profile") not in ("quiet", "balanced", "performance", "low-power", "cool", "balanced-performance"):
            raise ValueError("Invalid thermal profile")
    else:
        raise ValueError("Driver reconfiguration is unavailable in this build")
