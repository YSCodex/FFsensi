from __future__ import annotations

_C = "\033[96m" # Cyan
_G = "\033[92m" # Green
_Y = "\033[93m" # Yellow
_M = "\033[95m" # Magenta
_R = "\033[0m"  # Reset
_B = "\033[1m"  # Bold
_W = "\033[97m" # White

def print_banner() -> None:
    print(f"""{_C}{_B}┌──────────────────────────────────────────────────┐
│  {_W}YS SENSI ENGINE v2.5{_C}                            │
│  {_W}Advanced Device Benchmarking & Sensi Tuner{_C}      │
├──────────────────────────────────────────────────┤
│  {_Y}Owner:{_R} {_W}@ysyuvrajyt (Instagram){_C}                  │
│  {_Y}Telegram:{_R} {_W}t.me/YSCoder{_C}                          │
│            {_W}t.me/VibeCoderJantaParty{_C}              │
└──────────────────────────────────────────────────┘{_R}""")

def print_section(title: str) -> None:
    print(f"\n{_M}{_B}» {title}{_R}\n")

def print_success(message: str) -> None:
    print(f"{_G}[+]{_R} {message}")

def print_warning(message: str) -> None:
    print(f"{_Y}[!]{_R} {message}")