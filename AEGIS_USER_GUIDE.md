# 🛡️ AegisShield: Comprehensive User & Deployment Guide

Welcome to **AegisShield**, the world’s first Predictive Autonomous Security Defender. This guide outlines how to operate, monitor, and maintain your fully evolved security fortress.

## 🚀 The Master Command
To bootstrap the entire security stack (Daemon, AI, DDoS Shield, ART Lab, Deception, C2) and launch the Live HUD:
```bash
./shield.sh dashboard
```

## 🏗️ Core Architecture & Modules

### 1. The SOC (Security Operations Center) HUD
The centralized command center for real-time monitoring and narrative security.
- **Multi-Node C2:** Monitor and protect multiple project folders simultaneously.
- **Semantic Intelligence:** AI periodically reviews "Normal" traffic to detect slow-drip reconnaissance.
- **Story Feed:** Narrates every background action step-by-step.

### 2. Adaptive Cyber Deception (Morphing Defense)
AegisShield autonomously changes its identity to mislead attackers.
- **Blackberry Masquerade:** Pretends to be a BlackBerry Enterprise Server.
- **Safe Traps:** Dynamically opens ghost ports (FTP, RDP) that act as tripwires.
- **IP Quarantine:** Automatically "black-holes" any IP that touches a deception trap.

### 3. PAS (Predictive Active Shielding)
The "Response Engine" powered by a local **TinyLlama SLM**.
- **Autonomous Self-Healing:** The AI re-writes dangerous code in the Digital Twin and verifies it before reporting.
- **Logic Sentinel:** Deep semantic review of source code logic (understanding context).

### 4. DDoS & Network Shield (Tarpitting)
Active network-level defense.
- **Active Tarpitting:** Slows down suspicious IPs by holding connections for 15s to exhaust attacker resources.
- **Active Blocking:** Kernel-level firewall drops for aggressive DDoS bursts.

## 📊 Reporting & Maintenance

### The Professional Fix List (`FIX_LIST.md`)
Located in your **project root**, this is a consolidated checklist of vulnerabilities for all nodes.
- **Automation:** Refreshed every morning at 9:00 AM.

### Autonomous Garbage Collection
Ensures the system remains sustainable:
- **Log Rotation:** Automatically truncates logs if the folder exceeds 50MB.
- **Digital Twin Grooming:** Purges temporary artifacts to save disk space.

---

## 🛠️ Extended CLI Reference
| Command | Description |
| :--- | :--- |
| `start` / `stop` | Manage the entire background C2 fortress |
| `add-node <path>`| Add a new project directory to protect |
| `dashboard` | Bootstrap everything and open the HUD |
| `fix-list` | Generate the consolidated checklist for all nodes |
| `garbage-collect`| Manually trigger a storage cleanup |
| `simulate-breadcrumb`| Test the Canary Token detection |
| `simulate-masquerade`| Test HTTP header obfuscation |

---
**Final Status:** AegisShield v4.0 is fully deployed, automated, and protecting your server ecosystem.
