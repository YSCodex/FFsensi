from __future__ import annotations
from typing import Any
from core.device import DeviceInfo
from core.benchmark import BenchmarkResults, get_final_tier

SENSI_MAX = 200
SENSI_MIN = 1
SENSITIVITY_KEYS = ("g", "rd", "x2", "x4", "sn", "fl")
LABEL_MAP = {"g": "General", "rd": "Red Dot", "x2": "2x", "x4": "4x", "sn": "Sniper", "fl": "Free Look"}
RATIO_MAP = {"rd": 0.91, "x2": 0.83, "x4": 0.73, "sn": 0.67, "fl": 0.94}

def clamp_val(val: float, low: int = SENSI_MIN, high: int = SENSI_MAX) -> int:
    return max(low, min(high, int(round(val))))

def get_screen_dimensions(device: DeviceInfo) -> tuple[float, float]:
    width, height = device._w, device._y
    if width <= 0 or height <= 0:
        return 2400.0, 1.0
    diagonal = (width * width + height * height) ** 0.5
    return diagonal, (device._p or 400) / 400.0

def calculate_base_general(device: DeviceInfo, results: BenchmarkResults, final_tier: str) -> float:
    tier_base_map = {"budget": 98, "mid": 122, "upper_mid": 148, "flagship": 175}
    base_val = tier_base_map.get(final_tier, 122)
    base_val += (results._i - 50) * 0.92
    
    hz_bonus = {60: 0, 90: 9, 120: 16, 144: 20}.get(device._z or 60, 0)
    base_val += hz_bonus
    
    diagonal, density_factor = get_screen_dimensions(device)
    if diagonal >= 2600:
        base_val -= 10
    elif diagonal >= 2350:
        base_val -= 5
    elif diagonal < 2000:
        base_val += 5
    
    base_val -= (density_factor - 1.0) * 11
    
    if device._g > 0:
        if device._g < 4:
            base_val -= 14
        elif device._g < 6:
            base_val -= 7
        elif device._g >= 12:
            base_val += 8
            
    if results._h == "t":
        base_val -= 9
    if results._x > 2800:
        base_val += 7
    elif 0 < results._x < 1800:
        base_val -= 7
    if 0 < results._l < 8.0:
        base_val += 6
    elif results._l > 12.0:
        base_val -= 4
        
    base_val += results._b * 0.35
    base_val += results._u * 0.12
    return base_val

def check_headshot_bonus(device: DeviceInfo, results: BenchmarkResults, final_tier: str) -> float:
    bonus = 0.0
    if results._i >= 55 and final_tier in ("upper_mid", "flagship"):
        bonus += 6.0
    if 0 < results._l <= 10.0:
        bonus += 4.0
    if device._z >= 90:
        bonus += 3.0
    return bonus

def generate_sensitivity(device: DeviceInfo, results: BenchmarkResults, manual_tier: str | None = None) -> dict[str, Any]:
    tier = manual_tier or get_final_tier(device, results)
    general_score = clamp_val(calculate_base_general(device, results, tier) + check_headshot_bonus(device, results, tier))
    
    sensi_dict: dict[str, int] = {"g": general_score}
    for key, ratio in RATIO_MAP.items():
        sensi_dict[key] = clamp_val(general_score * ratio)
        
    sensi_dict["rd"] = clamp_val(min(sensi_dict["rd"], general_score - 6))
    sensi_dict["x2"] = clamp_val(min(sensi_dict["x2"], sensi_dict["rd"] - 9))
    sensi_dict["x4"] = clamp_val(min(sensi_dict["x4"], sensi_dict["x2"] - 11))
    sensi_dict["sn"] = clamp_val(min(sensi_dict["sn"], sensi_dict["x4"] - 9))
    sensi_dict["fl"] = clamp_val(max(sensi_dict["fl"], general_score - 14))
    
    if results._i >= 60:
        sensi_dict["rd"] = clamp_val(min(sensi_dict["rd"] + 2, general_score - 4))
        
    return {
        "sx": sensi_dict,
        "tr": tier,
        "pi": results._i,
        "mx": SENSI_MAX,
        "hs": check_headshot_bonus(device, results, tier) > 0,
    }

def format_sensi_output(device: DeviceInfo, results_payload: dict[str, Any], results: BenchmarkResults) -> str:
    sensi = results_payload["sx"]
    credit_line = "Owner: @ysyuvrajyt | TG: t.me/YSCoder & t.me/VibeCoderJantaParty"
    lines = [
        "=" * 54,
        "  YS EXTREME SENSI ENGINE",
        f"  {credit_line}",
        f"  SCALE 1-{SENSI_MAX}",
        "=" * 54,
        f"DEVICE : {device._n}",
        f"CHIP   : {device._h} / {device._r}",
        f"PANEL  : {device._w}x{device._y} @{device._z}Hz {device._p}dpi",
        f"RAM    : {device._g or '?'}GB | BATT {device._l}% | LOAD {device._q}",
        f"TOUCH  : {device._t or '?'}Hz | LAT {results._l}ms",
        f"POWER  : {results._i}/100 | GFXIDX {results._f} | BOOST {results._b}",
        f"TIER   : {results_payload['tr']} | HS_MODE {'ON' if results_payload['hs'] else 'OFF'}",
        "",
        "--- INGAME ---",
    ]
    for key in SENSITIVITY_KEYS:
        lines.append(f"{LABEL_MAP[key]:18}: {sensi[key]}")
    lines.extend(["", f"--- {credit_line} ---", "=" * 54])
    return "\n".join(lines)