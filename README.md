<p align="center">
  <img src="https://img.shields.io/github/stars/YSCodex/FFsensi?style=for-the-badge&color=FFE000&logo=github" alt="Stars">
  <img src="https://img.shields.io/github/forks/YSCodex/FFsensi?style=for-the-badge&color=00FFCC&logo=git" alt="Forks">
  <img src="https://img.shields.io/github/license/YSCodex/FFsensi?style=for-the-badge&color=0088FF" alt="License">
</p>

<h1 align="center">⚡ YS Extreme Sensi Engine ⚡</h1>

<p align="center">
  <b>Advanced hardware-driven device optimization, performance benchmarking, and custom sensitivity configuration utility for Android.</b>
</p>

<p align="center">
  <a href="https://t.me/YSCoder">
    <img src="https://img.shields.io/badge/YSCoder-Telegram_Channel-229ED9?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram 1">
  </a>
  <a href="https://t.me/VibeCoderJantaParty">
    <img src="https://img.shields.io/badge/Vibe_Coder_Janta_Party-Telegram_Group-229ED9?style=for-the-badge&logo=telegram&logoColor=white" alt="Telegram 2">
  </a>
</p>

<p align="center">
  <a href="https://instagram.com/ysyuvrajyt">
    <img src="https://img.shields.io/badge/ysyuvrajyt-Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white" alt="Instagram">
  </a>
</p>

---

## 📖 Introduction

**YS Sensi Engine** is a utility designed to inspect, benchmark, and optimize touch responsiveness and aiming parameters for gaming applications (specifically optimized for Free Fire). Rather than applying generic static values, this engine conducts active system diagnostics and stress benchmarks to build a highly optimized profile engineered specifically for your phone's processor, thermal limits, RAM bandwidth, and touch polling architecture.

Whether running on entry-level devices or standard high-end chipsets, the engine adjusts calculations to extract the most stable touch coordinates and aiming targets without causing frame pacing spikes or processing bottlenecks.

---

## ✨ Features & Capabilities

* 📱 **Active Hardware Diagnostics**: Inspects active board revisions, GPU drivers, display density (DPI), RAM size, and CPU load.
* ⚡ **Performance Benchmarking**: Runs mathematical float computations, logic stress routines, and physical memory copy latency sweeps.
* 🎯 **Dynamic Sensitivity Scale (1-200)**: Translates hardware capacity metrics into tailored sensitivity maps (General, Red Dot, Scopes, and Free Look).
* ⚙️ **Refresh Rate Synchronization**: Tailors values dynamically to match standard hardware screens operating at 60Hz, 90Hz, 120Hz, or 144Hz.
* 📄 **Multi-Format Exporting**: Produces a clear, readable text log (`output/sensi_*.txt`) and a structured JSON record (`output/report_*.json`).
* 🚀 **Shell Booster Generation**: Automatically compiles target tweaks (`output/performance_boost.sh` and `output/game_optimize.sh`) to regulate frame timing and memory caches.

---

## 🛠️ Performance Metrics Inspected

| Metric | Evaluated Target | Impact on Aiming |
|----------|----------|----------|
| **CPU Speed** | Micro-operations per second | Processing consistency & drag linearity |
| **Memory Bandwidth** | Data copy rate (MB/s) | Reduces touch input drops during intense frames |
| **Latency** | Active Touch rate (Hz) to Latency (ms) | Minimizes tap-to-render delays |
| **Load Average** | Active processor thermal / system stress | Corrects frame drops during high-activity scenarios |
| **Display Diagnostics** | Refresh rate (Hz) and density factor (DPI) | Smooths aiming paths & visual tracking |

---

## 📥 Terminal Installation Guides

You can install and execute this terminal package on terminal hosts (like Termux) using either the automated setup or the manual steps.

### Option 1: Quick Install (Auto-installer)

```bash
pkg install git python -y && git clone https://github.com/YSCodex/FFsensi.git && cd FFsensi && bash setup.sh
```

### Option 2: Manual Installation & Startup

#### 1. Keep target repository tools and packages updated

```bash
termux-change-repo
pkg update && pkg upgrade -y
pkg install git python -y
```

#### 2. Allow storage management permissions within Termux

```bash
termux-setup-storage
```

#### 3. Clone the repository and locate local directory

```bash
git clone https://github.com/YSCodex/FFsensi.git
cd FFsensi
```

#### 4. Launch the processing application

```bash
python main.py
```

---

## 🚀 Execution Modifiers

Use runtime flags to modify how the engine behaves during diagnostic runs:

```bash
# Execute standard benchmark and produce aiming parameters
python main.py

# Run a rapid scan using minimal benchmarking steps
python main.py --q

# Print all recognized device properties without running calculations
python main.py --info

# Perform device scan and generate game-booster shell commands
python main.py --qp

# Override model detection variables manually during execution
python main.py --m "My Custom Device"

# Iterate hardware checks specific number of times (e.g. 5) to average results
python main.py --rn 5
```

---

## 📁 Repository Structure

```text
FFsensi/
│
├── README.md               # User manual and configuration guide
├── main.py                 # Core command runner (CLI Entrypoint)
├── setup.sh                # Automation shell installation helper
├── LICENSE                 # Project open-source license terms
├── .gitignore              # Local file filters for GitHub
│
├── core/                   # Underlying calculations package
│   ├── __init__.py         # Package identification module
│   ├── device.py           # Device details and diagnostics
│   ├── benchmark.py        # CPU, GFX, Memory benchmarks
│   ├── sensi_generator.py  # Aim-scaling calculations
│   ├── booster.py          # Tuning script compiler
│   ├── ui.py               # ASCII Terminal UI layouts
│   └── device_tiers.json   # Processor target mappings database
│
└── output/                 # Results directory for compiled exports
```

---

## 🌐 Community & Support

Join the communities below to share configurations, request support, or participate in active system modification discussions:

| Resource | Target Destination |
|-----------|-----------|
| 🛡️ **Owner/Developer** | [ysyuvrajyt on Instagram](https://instagram.com/ysyuvrajyt) |
| 💻 **GitHub Repository** | [YSCodex/FFsensi on GitHub](https://github.com/YSCodex/FFsensi) |
| 📢 **Core Tech Channel** | [@YSCoder on Telegram](https://t.me/YSCoder) |
| 💬 **Community Discussions** | [@VibeCoderJantaParty on Telegram](https://t.me/VibeCoderJantaParty) |

---

## ⚖️ License & Disclaimer

- License: Distributed under the standard open-source MIT License.
- Disclaimer: This performance benchmarking engine computes recommended operational parameters and sensitivity maps. Application scripts containing system tweaks are intended for optimization purposes. Run booster scripts in compliance with target applications' policies.
