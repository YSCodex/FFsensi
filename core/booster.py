from __future__ import annotations
from pathlib import Path
from core.device import DeviceInfo

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = ROOT_DIR / "output"

def get_brand_specific_commands(brand: str) -> list[str]:
    tag = brand.lower()
    commands: list[str] = []
    if any(keyword in tag for keyword in ("xiaomi", "redmi", "poco")):
        commands.append("settings put system power_mode 1 2>/dev/null || true")
        commands.append("am start -a miui.intent.action.APP_MANAGER_GAME_MAIN 2>/dev/null || true")
    elif "samsung" in tag:
        commands.append("am start -n com.samsung.android.game.gametools/.ui.MainActivity 2>/dev/null || true")
    elif "realme" in tag or "oppo" in tag:
        commands.append("am start -n com.coloros.gamespaceui/.activity.StartActivity 2>/dev/null || true")
    elif "vivo" in tag or "iqoo" in tag:
        commands.append("am start -n com.vivo.gamecube/.ui.GameCubeMainActivity 2>/dev/null || true")
    elif "oneplus" in tag:
        commands.append("am start -n com.oneplus.gamespace/.ui.GameSpaceMainActivity 2>/dev/null || true")
    return commands

def generate_boost_script(device: DeviceInfo) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / "performance_boost.sh"
    brand_cmds = "\n".join(get_brand_specific_commands(device._b))
    script_content = f"""#!/system/bin/sh
set -e
settings put global window_animation_scale 0.0 2>/dev/null || true
settings put global transition_animation_scale 0.0 2>/dev/null || true
settings put global animator_duration_scale 0.0 2>/dev/null || true
settings put global force_gpu_rasterization 1 2>/dev/null || true
settings put global hardware_rendering 1 2>/dev/null || true
settings put system peak_refresh_rate {device._z or 120} 2>/dev/null || true
settings put system min_refresh_rate 60 2>/dev/null || true
cmd deviceidle whitelist +com.dts.freefireth 2>/dev/null || true
cmd deviceidle whitelist +com.dts.freefiremax 2>/dev/null || true
for _pkg in com.dts.freefireth com.dts.freefiremax; do
  cmd game mode set "$_pkg" 2 2>/dev/null || true
  cmd game mode performance "$_pkg" enable 2>/dev/null || true
  cmd netd setprio "$_pkg" 1 2>/dev/null || true
done
{brand_cmds}
echo OK
"""
    path.write_text(script_content, encoding="utf-8", newline="\n")
    return path

def generate_optimize_script(device: DeviceInfo) -> Path:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUTPUT_DIR / "game_optimize.sh"
    script_content = f"""#!/system/bin/sh
am force-stop com.dts.freefireth 2>/dev/null || true
am force-stop com.dts.freefiremax 2>/dev/null || true
cmd activity kill-all 2>/dev/null || true
sync
echo OK
"""
    path.write_text(script_content, encoding="utf-8", newline="\n")
    return path