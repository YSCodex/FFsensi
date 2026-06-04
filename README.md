# YS Extreme Sensi Engine

YS Sensi is an advanced device-specific performance benchmarking utility and sensitivity optimization tool designed to customize gaming parameters for a fluid touch response and consistent aim control. Unlike standard generalized configurations, this utility performs real-time benchmarking on device specifications to compute personalized sensitivity scales based directly on processing capabilities.

The tool measures multiple device performance factors—including active CPU speed, memory copy bandwidth, screen refresh rate, active system load, touch response rate, and current battery levels—to generate an accurate custom sensitivity profile.

Whether operating on mid-range hardware or flagship devices, YS Sensi adjusts scaling parameters to leverage maximum target alignment, smoother control mechanics, and enhanced refresh compatibility.

---

### 🚀 Key Capabilities

* 📱 **Hardware Architecture Detection** - Inspects processor attributes, system manufacturer, and active memory allocation.
* ⚡ **Live Performance Benchmarking** - Conducts focused CPU operations, memory bandwidth checks, and lightweight mathematical float stress tests.
* 🎯 **Dynamic Sensitivity Scale** - Employs a custom logic to compute General, Red Dot, 2x, 4x, Sniper, and Free Look sensitivities (scaled 1-200).
* 📄 **Structured File Export** - Stores detailed scan profiles in structured `.json` reports and `.txt` reference files.
* 🛠️ **Optimization Script Generation** - Exports system-level tuning instructions (`performance_boost.sh` and `game_optimize.sh`) to streamline refresh targets and manage memory usage.
* 💻 **Compatible Environment** - Fully compatible with terminal interfaces such as Termux on Android.

---

## 📥 Installation & Usage

To download, configure, and execute the engine on terminal clients (like Termux), execute the following commands in order:

### Quick Setup (Auto-Installer)

```bash
pkg install git python -y && git clone https://github.com/YSCodex/FFsensi.git && cd FFsensi && bash setup.sh