import ast
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "service"))
from control_policy import validate_command, peer_allowed

class PolicyTests(unittest.TestCase):
    def test_peers(self):
        self.assertTrue(peer_allowed(1000,1000))
        self.assertTrue(peer_allowed(0,1000))
        self.assertFalse(peer_allowed(1001,1000))
    def test_controls(self):
        validate_command("set_battery_limiter", {"enabled":True})
        validate_command("set_fan_speed", {"cpu":0,"gpu":0})
        validate_command("set_per_zone_mode", dict(zone1="ffffff",zone2="ff0000",zone3="00ff00",zone4="0000ff",brightness=25))
    def test_invalid_and_driver_commands(self):
        for command, params in [("set_fan_speed",{"cpu":-1,"gpu":100}), ("set_fan_speed",{"cpu":True,"gpu":100}), ("set_battery_limiter",{"enabled":"false"}), ("set_per_zone_mode",{"zone1":"ff\n", "brightness":25}), ("force_enable_all",{}), ("set_modprobe_parameter_nitro",{}), ("restart_drivers_and_daemon",{})]:
            with self.subTest(command=command), self.assertRaises(ValueError):
                validate_command(command,params)
    def test_startup_has_no_restore_or_reload(self):
        tree=ast.parse((Path(__file__).resolve().parents[1]/"service/nitrosense-daemon.py").read_text())
        for cls in tree.body:
            if isinstance(cls,ast.ClassDef) and cls.name in ("HardwareManager","NitroSenseDaemon"):
                for method in cls.body:
                    if isinstance(method,ast.FunctionDef) and method.name in ("__init__","setup","run"):
                        for call in ast.walk(method):
                            if isinstance(call,ast.Call):
                                name=getattr(call.func,"id",getattr(call.func,"attr",""))
                                self.assertNotIn(name,{"restore_fan","restore_lighting","restore_power_mode","_restart_drivers_and_daemon","start_monitoring"})
if __name__=="__main__": unittest.main()
