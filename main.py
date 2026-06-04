#!/usr/bin/env python3
from __future__ import annotations
import argparse
import json
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from core.device import detect_device, get_device_info_dict
from core.benchmark import run_benchmarks
from core.sensi_generator import generate_sensitivity, format_sensi_output
from core.booster import generate_boost_script, generate_optimize_script
from core.ui import print_banner, print_section, print_success, print_warning

OUTPUT_DIR = ROOT_DIR / "output"

def reconfigure_encoding() -> None:
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure and callable(reconfigure):
            try:
                reconfigure(encoding="utf-8", errors="replace")
            except (OSError, ValueError):
                pass

def clean_filename(name: str) -> str:
    return "".join(c if c.isalnum() else "_" for c in name.lower()).strip("_")[:48]

def save_results(device, benchmark, results) -> tuple[Path, Path]:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_name = clean_filename(device._n)
    txt_path = OUTPUT_DIR / f"sensi_{safe_name}.txt"
    json_path = OUTPUT_DIR / f"report_{safe_name}.json"
    
    payload = {
        "device_info": get_device_info_dict(device),
        "benchmark_results": benchmark._d(),
        "sensitivity_results": results
    }
    
    txt_path.write_text(format_sensi_output(device, results, benchmark), encoding="utf-8")
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    return txt_path, json_path

def run_main(device, is_quick: bool, generate_scripts: bool, cpu_time: float, mem_time: float, gfx_time: float, runs: int) -> None:
    print_banner()
    print_section(device._n)
    print_warning("SCANNING DEVICE HARDWARE & PERFORMANCE...")
    
    benchmark = run_benchmarks(device, cpu_time, mem_time, gfx_time, runs)
    
    print_section("BENCHMARK RESULTS")
    print(f"  POWER SCORE  : {benchmark._i}/100")
    print(f"  CPU SPEED    : {benchmark._c:,.0f} ops/s")
    print(f"  RAM BANDWIDTH: {benchmark._m} MB/s")
    print(f"  GFX INDEX    : {benchmark._f}")
    print(f"  DEVICE TIER  : {benchmark._e.upper()}")
    print(f"  LATENCY      : {benchmark._l} ms")
    print(f"  BOOST INDEX  : {benchmark._b}")
    
    results = generate_sensitivity(device, benchmark)
    print("\n" + format_sensi_output(device, results, benchmark))
    
    txt_file, json_file = save_results(device, benchmark, results)
    print_success(f"Saved text results: {txt_file}")
    print_success(f"Saved json report : {json_file}")
    
    if generate_scripts:
        print_success(f"Generated Boost Script: {generate_boost_script(device)}")
        print_success(f"Generated Game Optimizer: {generate_optimize_script(device)}")

def main() -> int:
    reconfigure_encoding()
    parser = argparse.ArgumentParser(description="YS Sensi Engine CLI")
    parser.add_argument("--info", "-i", action="store_true", help="Show detected device info and exit")
    parser.add_argument("--qp", action="store_true", help="Generate optimization scripts")
    parser.add_argument("--q", action="store_true", help="Quick scan mode")
    parser.add_argument("--m", type=str, default=None, help="Manually override device name")
    parser.add_argument("--rn", type=int, default=3, help="Number of benchmark runs")
    args = parser.parse_args()
    
    device = detect_device(args.m)
    if args.info:
        for key, val in get_device_info_dict(device).items():
            print(f"  {key}: {val}")
        return 0
        
    cpu_t, mem_t, gfx_t = (1.0, 0.7, 0.5) if args.q else (2.0, 1.2, 0.9)
    run_main(device, args.q, args.qp, cpu_t, mem_t, gfx_t, max(1, args.rn))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())