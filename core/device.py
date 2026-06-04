from __future__ import annotations
import os
import platform
import re
import subprocess
from dataclasses import dataclass, asdict
from typing import Optional

@dataclass
class DeviceInfo:
    _b: str = "unknown"  # Brand
    _f: str = "unknown"  # Manufacturer
    _m: str = "unknown"  # Model
    _d: str = "unknown"  # Device name
    _h: str = "unknown"  # Hardware
    _r: str = "unknown"  # Board
    _s: str = "unknown"  # System Version (Android release)
    _k: str = "unknown"  # SDK Version
    _g: float = 0.0     # RAM Size (GB)
    _z: int = 60        # Refresh rate (Hz)
    _w: int = 0         # Screen width
    _y: int = 0         # Screen height
    _p: int = 0         # DPI Density
    _t: int = 0         # Touch sampling rate
    _l: int = 100       # Battery level
    _q: float = 0.0     # System load average

    @property
    def _n(self) -> str:
        brand, model = self._b.strip(), self._m.strip()
        if brand.lower() in ("unknown", "") and model.lower() != "unknown":
            return model
        if model.lower() in ("unknown", ""):
            return brand
        return f"{brand} {model}".strip()

    @property
    def _x(self) -> str:
        return f"{self._b} {self._m} {self._d} {self._h}".lower()

def run_command(cmd: list[str]) -> str:
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=8, check=False)
        return (result.stdout or result.stderr or "").strip()
    except (OSError, subprocess.TimeoutExpired):
        return ""

def get_system_property(key: str) -> str:
    val = run_command(["getprop", key]) or run_command(["/system/bin/getprop", key])
    return val or ""

def parse_resolution(text: str) -> tuple[int, int]:
    match = re.search(r"(\d{3,4})x(\d{3,4})", text)
    return (int(match.group(1)), int(match.group(2))) if match else (0, 0)

def parse_density(text: str) -> int:
    match = re.search(r"(\d+)\s*dpi", text, re.I)
    return int(match.group(1)) if match else 0

def get_total_ram() -> float:
    try:
        with open("/proc/meminfo", encoding="utf-8") as f:
            for line in f:
                if line.startswith("MemTotal:"):
                    return round(int(line.split()[1]) / (1024 * 1024), 1)
    except OSError:
        pass
    return 0.0

def get_refresh_rate() -> int:
    for path in ("/sys/class/graphics/fb0/mode", "/sys/class/drm/sde-crtc-0/mode"):
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read().lower()
            for hz in (144, 120, 90, 60):
                if f"{hz}" in text:
                    return hz
        except OSError:
            continue
    dumpsys = run_command(["dumpsys", "display"])
    for hz in (144, 120, 90):
        if re.search(rf"\b{hz}\s*hz\b", dumpsys, re.I):
            return hz
    return 60

def get_touch_rate() -> int:
    for path in ("/sys/class/input/input0/sampling_rate", "/sys/class/input/input1/sampling_rate"):
        try:
            with open(path, encoding="utf-8") as f:
                return int(float(f.read().strip()))
        except (OSError, ValueError):
            continue
    return 0

def get_battery_level() -> int:
    dumpsys = run_command(["dumpsys", "battery"])
    match = re.search(r"level:\s*(\d+)", dumpsys)
    return int(match.group(1)) if match else 100

def get_cpu_load() -> float:
    try:
        load = os.getloadavg()[0]
        return round(load, 2)
    except (OSError, AttributeError):
        return 0.0

def detect_device(manual_name: Optional[str] = None) -> DeviceInfo:
    if manual_name:
        return DeviceInfo(_b="manual", _f="manual", _m=manual_name, _d=manual_name.replace(" ", "_").lower())
    if not (os.path.isdir("/system") or get_system_property("ro.product.model")) and platform.system() == "Windows":
        return DeviceInfo(_b="demo", _f="pc", _m=platform.node() or "pc", _s="0")
    
    info = DeviceInfo(
        _b=get_system_property("ro.product.brand") or get_system_property("ro.product.vendor.brand"),
        _f=get_system_property("ro.product.manufacturer"),
        _m=get_system_property("ro.product.model"),
        _d=get_system_property("ro.product.device"),
        _h=get_system_property("ro.hardware"),
        _r=get_system_property("ro.product.board"),
        _s=get_system_property("ro.build.version.release"),
        _k=get_system_property("ro.build.version.sdk"),
        _g=get_total_ram(),
        _z=get_refresh_rate(),
        _t=get_touch_rate(),
        _l=get_battery_level(),
        _q=get_cpu_load(),
    )
    wm_size = run_command(["wm", "size"]) or run_command(["/system/bin/wm", "size"])
    info._w, info._y = parse_resolution(wm_size)
    wm_density = run_command(["wm", "density"]) or run_command(["/system/bin/wm", "density"])
    info._p = parse_density(wm_density)
    return info

def get_device_info_dict(info: DeviceInfo) -> dict:
    return asdict(info)