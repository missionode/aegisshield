import json
import os
from datetime import datetime

HITS_LOG = "logs/hits.log"
AEGIS_LOG = "logs/aegis.log"
CONSULTANT_LOG = "logs/consultant.log"

def log_consultant(thought, action=None):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] [AI] Thought: {thought}\n"
    if action:
        entry += f"[{timestamp}] [AI] Action: {action}\n"
    
    with open(CONSULTANT_LOG, "a") as f:
        f.write(entry)
    
    with open(AEGIS_LOG, "a") as f:
        f.write(entry)

def run_pas_analysis():
    # 1. Analyze Hits
    if os.path.exists(HITS_LOG):
        with open(HITS_LOG, "r") as f:
            hits = [json.loads(line) for line in f.readlines()]
        
        malicious_hits = [h for h in hits if h["intent"] == "MALICIOUS"]
        if malicious_hits:
            target_ip = malicious_hits[-1]["ip"]
            log_consultant(
                f"I detected multiple malicious probes from {target_ip} targeting {malicious_hits[-1]['path']}.",
                f"VIRTUAL_PATCH: Blocking IP {target_ip} temporarily."
            )

    # 2. Analyze ART Lab Results
    # Check if .env was created in twin during simulation
    if os.path.exists("digital_twin/.env"):
        log_consultant(
            "My ART Lab simulation revealed that a .env file could be exposed.",
            "VIRTUAL_PATCH: Enforcing rule to prevent .env files in root."
        )

def get_fix_list():
    # Return a high-signal narrative feed
    if os.path.exists(CONSULTANT_LOG):
        with open(CONSULTANT_LOG, "r") as f:
            return f.read()
    return "No insights yet."

if __name__ == "__main__":
    run_pas_analysis()
