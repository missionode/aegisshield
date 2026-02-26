import os
import json
import subprocess
import re
from datetime import datetime
from slm_inference import AegisSLM

FINGERPRINT_FILE = "logs/system_fingerprint.json"
DECEPTION_PLAN = "logs/deception_plan.json"
STORY_LOG = "logs/story.log"

def log_story(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    try:
        with open(STORY_LOG, "a") as f:
            f.write(f"[{timestamp}] 🧠 SLM Planner: {message}\n")
    except: pass

def get_active_ports():
    used_ports = set()
    try:
        result = subprocess.run(["lsof", "-iTCP", "-sTCP:LISTEN", "-n", "-P"], capture_output=True, text=True)
        for line in result.stdout.splitlines()[1:]:
            parts = line.split()
            if len(parts) > 8:
                port_str = parts[8].split(':')[-1]
                try: used_ports.add(int(port_str))
                except: pass
    except: pass
    return list(used_ports)

def discover_trusted_ips(root_dir):
    trusted = {"127.0.0.1", "::1"}
    ip_regex = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    for root, dirs, files in os.walk(root_dir):
        if any(exc in root for exc in ["venv", "node_modules", ".git", "digital_twin"]): continue
        for f in files:
            if f.endswith((".py", ".js", ".conf", ".env")):
                try:
                    with open(os.path.join(root, f), 'r', errors='ignore') as file:
                        content = file.read()
                        found_ips = re.findall(ip_regex, content)
                        for ip in found_ips:
                            if ip.startswith(("127.", "192.168.", "10.")): trusted.add(ip)
                except: pass
    return list(trusted)

def intellectual_bootstrap(root_dir):
    log_story("Requesting Intellectual Determination from SLM...")
    
    # 1. Collect Context
    files = [f for f in os.listdir(root_dir) if os.path.isfile(os.path.join(root_dir, f))]
    file_manifest = ", ".join(files[:15]) # Send top 15 files
    used_ports = get_active_ports()
    trusted_ips = discover_trusted_ips(root_dir)

    # 2. Call SLM
    slm = AegisSLM()
    raw_strategy = slm.determine_strategy(file_manifest, used_ports)
    
    try:
        # Try to parse the JSON from SLM
        strategy = json.loads(re.search(r'\{.*\}', raw_strategy, re.DOTALL).group())
    except:
        # Fallback if SLM output is messy
        strategy = {
            "tech_stack": "Unknown/Generic",
            "deceptive_server": "BlackBerry-Enterprise-Server/5.0.3",
            "ghost_ports": [21, 2222, 3389, 5900]
        }

    # 3. Store Results
    fingerprint = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "slm_determination": strategy,
        "trusted_ips": trusted_ips,
        "used_ports": used_ports,
        "root": os.path.abspath(root_dir)
    }

    if not os.path.exists("logs"): os.makedirs("logs")
    with open(FINGERPRINT_FILE, "w") as f:
        json.dump(fingerprint, f, indent=4)
    
    deception_plan = {
        "real_stack": strategy.get("tech_stack", "Unknown"),
        "deceptive_server": strategy.get("deceptive_server", "BlackBerry"),
        "trap_ports": strategy.get("ghost_ports", [2222, 3389]),
        "honey_endpoints": ["/admin-portal", "/.env.backup", "/phpmyadmin"],
        "whitelist": trusted_ips
    }
    with open(DECEPTION_PLAN, "w") as f:
        json.dump(deception_plan, f, indent=4)

    log_story(f"SLM Intellectual determination complete. Stack: {deception_plan['real_stack']}. Deception: {deception_plan['deceptive_server']}")
    return fingerprint

if __name__ == "__main__":
    import sys
    intellectual_bootstrap(sys.argv[1] if len(sys.argv) > 1 else "..")
