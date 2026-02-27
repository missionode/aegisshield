# 🛡️ AegisShield: Universal AI Security Controller (C2)

**AegisShield** is a professional-grade, **Predictive Autonomous Security Defender**. It evolves your server from a passive target into a **Thinking, Deceptive Fortress**. By combining local Small Language Models (SLM) with active network countermeasures, it identifies, traps, and neutralizes threats across multiple projects simultaneously.

---

## 🏗️ Core Architecture & Modules

### 1. Semantic Intelligence (v4.0 SOC HUD)
The centralized command center for real-time monitoring. AegisShield doesn't just match patterns—it understands logic using a local Small Language Model (SLM) ecosystem.
- **Intellectual SOC Analyst:** Evaluates web traffic intents strictly against advanced OWASP Top 10 and MITRE ATT&CK hacking methodologies, providing narrative defense theories.
- **Semantic Payload Inspection (AI WAF):** A 100% safe, background AI Web Application Firewall that queue-reads suspicious payloads to catch obfuscated zero-days that regex rules miss.
- **Semantic SLM Anti-Virus & Active Quarantine:** Real-time localized file scanning that leverages SLM-generated research signatures and deep semantic verification. Upon definitive malware detection, AegisShield automatically neutralizes and moves the threat to a secure `quarantine/` folder. This physical file-system quarantine is **100% tech-stack independent** and works identically whether the malicious script is PHP, Python, Node, Bash, or Perl.
- **Autonomous Threat Intel:** Pulls official CISA RSA advisories and generates proactive "Ethical Pen-Testing Strategies" to your local wiki.
- **Secure Auto-Upgrades:** Before updating the local TinyLlama model, the C2 daemon checks HuggingFace API compatibility, blocking architectural changes that risk stability and pushing manual alerts to the HUD.

### 2. PAS (Predictive Active Shielding)
The "Response Engine" powered by the local SLM.
- **Autonomous Self-Healing:** The AI re-writes dangerous code in a sandboxed Digital Twin, tests the context, and verifies the solution before reporting it.
- **Logic Sentinel & Scanner Memory:** Deep semantic review of source code logic. To optimize performance, the scanner mathematically memorizes previously hardened snippets so it instantly ignores them during future scans, saving zero-day compute power.

### 3. Adaptive Cyber Deception (Morphing Defense)
Mislead attackers by dynamically changing your server's fingerprint.
- **The Masquerade:** Automatically detects your underlying tech stack and alters HTTP headers to masquerade as a different legacy server (e.g., BlackBerry BES), frustrating automated enumeration tools.
- **Ghost Tripwires:** Dynamically opens high-value ghost ports (FTP, RDP) that act as silent alarms.
- **Immediate IP Quarantine:** Automatically "black-holes" any IP that touches a deception trap using kernel-level firewall rules.

### 4. Continuous Threat Intelligence & Ethical Hacking
Your C2 daemon connects locally to authoritative global feeds.
- **CISA RSS Sync:** Running `update-wiki` asynchronously fetches the latest Cybersecurity Advisories directly from CISA.
- **AI Wiki Generation:** For each new threat, the intellectual AI formats a new `.md` Wiki entry encompassing a Threat Overview, Prevention steps, and autonomously generates an **Ethical Pen-Testing Strategy**.

### 5. Active Tarpitting & Anti-DDoS
Active, resource-exhaustion defense at the network layer.
- **Active Tarpitting:** Slows down suspicious IPs by holding connections open for extended periods (15 seconds or more) to exhaust attacker resources and break automated scanners.
- **Active Blocking:** Kernel-level firewall drops for aggressive, high-volume DDoS bursts.

---

## 🚀 Deployment & Operation

Launch the full-screen Security HUD. On first start, AegisShield will automatically build an isolated Python virtual environment (`venv`) and install all required ML dependencies (`torch`, `transformers`) so it doesn't conflict with your OS.

```bash
cd aegisshield
./shield.sh dashboard
```

If you need to run specific `.py` files manually or interact with the Python environment directly, you should activate the virtual environment first:

```bash
cd aegisshield
source venv/bin/activate
# Now you can run commands like: python3 hit_monitor.py
```

### 📋 Consolidated Actionable Intelligence: `FIX_LIST.md`
A master checklist generated in your project root, providing:
- **Precise Locations:** Exact file and line numbers.
- **AI-Generated Fixes:** Direct code rewrites for logic flaws.
- **Multi-Node Coverage:** A single report for every directory under AegisShield protection.

### 🧹 Autonomous Garbage Collection
Ensures the system remains lightweight and sustainable:
- **Log Rotation:** Automatically truncates logs if the folder exceeds size thresholds.
- **Digital Twin Grooming:** Purges temporary artifacts to save disk space after scans complete.
- **SLM Tech-Stack Scavenger:** Analyzes your project's technology stack to dynamically identify and autonomously clean up temporary files, caches, or build artifacts (`.pyc`, `node_modules`).

---

## 🛠️ Management CLI Reference

Control the multi-node background daemon and trigger specific actions via `shield.sh`:

| Command | Description |
| :--- | :--- |
| `./shield.sh start` / `stop` | Manually start or stop the AegisShield background daemon. |
| `./shield.sh status` | Check if the daemon is active and list all protected nodes. |
| `./shield.sh dashboard` | Bootstrap all services and launch the interactive Security HUD. |
| `./shield.sh add-node <path>` | Register a new project directory for continuous SLM protection. |
| `./shield.sh run-analysis` | Force an immediate AI vulnerability scan across all registered nodes. |
| `./shield.sh fix-list` | Manually trigger the generation of the `FIX_LIST.md` report. |
| `./shield.sh update-wiki` | Force an update of the local Threat Intelligence Wiki. |
| `./shield.sh simulate-trap <path>` | Test the Morphing Deception logic on a specific node. |
| `./shield.sh simulate-breadcrumb` | Test the Canary Token (breadcrumb) injection. |
| `./shield.sh garbage-collect` | Manually trigger storage optimization (log rotation, twin cleanup). |
| `./shield.sh setup-cron` | Install system-level persistence for the heartbeat. |

---

**Status:** AegisShield v4.0 Stable is active and protecting your ecosystem.
