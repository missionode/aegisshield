# 🛡️ AegisShield: Universal AI Security Controller (C2)

**AegisShield** is a professional-grade, autonomous security framework. It evolves your server from a passive target into a **Thinking, Deceptive Fortress**. By combining local Small Language Models (SLM) with active network countermeasures, it identifies, traps, and neutralizes threats across multiple projects simultaneously.

---

## 🏗️ The C2 (Command & Control) Architecture

### 🤖 Semantic Intelligence (v4.0)
AegisShield doesn't just match patterns—it understands logic using a local Small Language Model (SLM) ecosystem.
- **Intellectual SOC Analyst:** Evaluates web traffic intents strictly against advanced OWASP Top 10 and MITRE ATT&CK hacking methodologies, providing narrative defense theories.
- **Semantic Payload Inspection (AI WAF):** A 100% safe, background AI Web Application Firewall that queue-reads suspicious payloads to catch obfuscated zero-days that regex rules miss.
- **Self-Healing Code with Scanner Memory:** The AI autonomously re-writes dangerous code in a sandbox (Digital Twin). It mathematically memorizes previously hardened snippets so it skips re-processing them in the future.
- **Autonomous Threat Intel:** Pulls official CISA RSA advisories and generates proactive "Ethical Pen-Testing Strategies" to your local wiki.
- **Secure SLM Upgrades:** Before updating the local TinyLlama model, the C2 daemon checks HuggingFace API compatibility, blocking architectural changes that risk stability and pushing manual alerts to the HUD.

### 🎭 Morphing Deception
Mislead attackers by dynamically changing your server's fingerprint.
- **The Masquerade:** Automatically detects your underlying tech stack and alters HTTP headers to masquerade as a different legacy server (e.g., BlackBerry BES), frustrating automated enumeration tools.
- **Ghost Tripwires:** Opens non-responsive, high-value ports (FTP, RDP) as silent alarms. Any connection attempt triggers an immediate kernel-level IP quarantine via iptables.

### 🕸️ Active Tarpitting & Anti-DDoS
Exhaust attacker resources and mitigate floods before they impact application performance.
- **Active Tarpitting:** AegisShield actively holds suspicious connections open for extended periods (15s+), intentionally slowing down scanners and brute-force bots to a crawl.
- **Dynamic Rate Limiting:** Monitors hits in real-time and scales defenses during high-volume DDoS attacks.

---

## 🚀 Deployment

Launch the full-screen Security HUD:

```bash
cd aegisshield
./shield.sh dashboard
```

### 📋 Consolidated Actionable Intelligence: `FIX_LIST.md`
A master checklist generated in your project root, providing:
- **Precise Locations:** Exact file and line numbers.
- **AI-Generated Fixes:** Direct code rewrites for logic flaws.
- **Multi-Node Coverage:** A single report for every directory under AegisShield protection.

---

## 🛠️ Management CLI Reference

Control the multi-node background daemon and trigger specific actions:

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
