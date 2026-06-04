from __future__ import annotations
import json
import os
import time
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any
from core.device import DeviceInfo

CPU_REF_OPS = 120_000_000.0
MEM_REF_SPEED = 800.0
GFX_REF_SCORE = 2_500_000.0

@dataclass
class BenchmarkResults:
    _c: float = 0.0  # CPU score
    _m: float = 0.0  # MEM speed
    _n: int = 1      # Cores
    _x: float = 0.0  # Freq
    _g: float = 0.0  # GFX math score
    _t: float = 0.0  # Duration
    _i: float = 0.0  # Power index (0-100)
    _e: str = "mid"  # Performance Tier
    _h: str = "n"    # Throttling detected (t/n)
    _u: float = 0.0  # Game power modifier
    _f: float = 0.0  # GFX index
    _l: float = 0.0  # Touch latency
    _b: float = 0.0  # Boost offset

    def _d(self) -> dict[str, Any]:
        return asdict(self)

def cpu_stress_test(seconds: float) -> float:
    start, deadline, seed, ops = time.perf_counter(), time.perf_counter() + seconds, 123456789, 0
    while time.perf_counter() < deadline:
        seed = (seed * 1103515245 + 12345) & 0x7FFFFFFF
        seed ^= seed >> 13
        ops += 1
    return ops / max(time.perf_counter() - start, 0.001)

def mem_bandwidth_test(seconds: float) -> float:
    size = 4 * 1024 * 1024
    try:
        buf_a, buf_b = bytearray(size), bytearray(size)
    except MemoryError:
        return 0.0
    start, deadline, bytes_copied = time.perf_counter(), time.perf_counter() + seconds, 0
    while time.perf_counter() < deadline:
        buf_b[:] = buf_a
        buf_a[0] = (buf_a[0] + 1) % 256
        bytes_copied += size * 2
    return (bytes_copied / (1024 * 1024)) / max(time.perf_counter() - start, 0.001)

def gfx_math_test(seconds: float) -> float:
    start, deadline, acc = time.perf_counter(), time.perf_counter() + seconds, 0.0
    while time.perf_counter() < deadline:
        for i in range(64):
            acc += (i * 1.41421356) ** 0.5
    return acc / max(time.perf_counter() - start, 0.001)

def get_cpu_cores() -> int:
    try:
        return os.cpu_count() or 1
    except OSError:
        return 1

def get_max_cpu_freq() -> float:
    max_freq = 0.0
    try:
        base_dir = "/sys/devices/system/cpu"
        for node in os.listdir(base_dir):
            if not node.startswith("cpu") or node == "cpufreq":
                continue
            path = f"{base_dir}/{node}/cpufreq/cpuinfo_max_freq"
            if os.path.isfile(path):
                with open(path, encoding="utf-8") as f:
                    max_freq = max(max_freq, int(f.read().strip()) / 1000.0)
    except OSError:
        pass
    return max_freq

def calculate_tier(power_index: float) -> str:
    if power_index >= 78:
        return "flagship"
    if power_index >= 58:
        return "upper_mid"
    if power_index >= 38:
        return "mid"
    return "budget"

def check_database_tier(hardware: str, board: str, search_tag: str) -> str:
    path = Path(__file__).resolve().parent / "device_tiers.json"
    if not path.is_file():
        return "mid"
    with open(path, encoding="utf-8") as f:
        tiers_db = json.load(f)
    search_haystack = f"{hardware} {board} {search_tag}".lower()
    order = ["flagship", "upper_mid", "mid", "budget"]
    best_tier = "mid"
    for chip_name, tier_val in tiers_db.items():
        if chip_name in search_haystack and order.index(tier_val) > order.index(best_tier):
            best_tier = tier_val
    return best_tier

def calculate_game_power(device: DeviceInfo) -> float:
    score = 50.0
    if device._t >= 240:
        score += 18
    elif device._t >= 120:
        score += 10
    if device._z >= 120:
        score += 8
    if device._l >= 50:
        score += 5
    if device._l < 20:
        score -= 12
    if device._q > 4.0:
        score -= 10
    elif device._q > 2.5:
        score -= 5
    return max(0.0, min(100.0, score))

def calculate_raw_performance(cpu: float, mem: float, gfx: float, cores: int, freq: float, game_power: float, boost_val: float) -> float:
    cpu_score = min(100.0, (cpu / CPU_REF_OPS) * 100.0)
    mem_score = min(100.0, (mem / MEM_REF_SPEED) * 100.0)
    gfx_score = min(100.0, (gfx / GFX_REF_SCORE) * 100.0)
    cores_bonus = min(12.0, max(0, (cores - 4) * 2.5))
    freq_bonus = min(15.0, (freq - 1500) / 50.0) if freq > 0 else 0.0
    return min(100.0, cpu_score * 0.42 + mem_score * 0.22 + gfx_score * 0.12 + cores_bonus + freq_bonus + game_power * 0.18 + boost_val * 0.06)

def run_benchmarks(device: DeviceInfo, cpu_t: float = 2.0, mem_t: float = 1.2, gfx_t: float = 0.9, runs: int = 3) -> BenchmarkResults:
    cores, freq = get_cpu_cores(), get_max_cpu_freq()
    cpu_runs, mem_runs, gfx_runs = [], [], []
    for _ in range(max(1, runs)):
        cpu_runs.append(cpu_stress_test(cpu_t))
        mem_runs.append(mem_bandwidth_test(mem_t))
        gfx_runs.append(gfx_math_test(gfx_t))
    
    cpu_avg = sum(cpu_runs) / len(cpu_runs)
    mem_avg = sum(mem_runs) / len(mem_runs)
    gfx_avg = sum(gfx_runs) / len(gfx_runs)
    game_power = calculate_game_power(device)
    boost_val = 8.0 if device._l >= 40 and device._q < 2.0 else 0.0
    
    raw_index = calculate_raw_performance(cpu_avg, mem_avg, gfx_avg, cores, freq, game_power, boost_val)
    quick_cpu = cpu_stress_test(0.7)
    throttling = "t" if quick_cpu < cpu_avg * 0.72 else "n"
    if throttling == "t":
        raw_index *= 0.9
    
    latency = max(4.0, 1000.0 / device._t) if device._t > 0 else 16.0
    return BenchmarkResults(
        _c=round(cpu_avg, 0),
        _m=round(mem_avg, 1),
        _n=cores,
        _x=round(freq, 0),
        _g=round(gfx_avg, 0),
        _t=round(cpu_t * runs + mem_t + gfx_t + 0.7, 1),
        _i=round(raw_index, 1),
        _e=calculate_tier(raw_index),
        _h=throttling,
        _u=round(game_power, 1),
        _f=round(gfx_avg / max(cpu_avg, 1) * 1000, 2),
        _l=round(latency, 2),
        _b=round(boost_val, 1),
    )

def get_final_tier(device: DeviceInfo, results: BenchmarkResults) -> str:
    db_tier = check_database_tier(device._h, device._r, device._x)
    order = ["budget", "mid", "upper_mid", "flagship"]
    return order[max(order.index(results._e), order.index(db_tier))]