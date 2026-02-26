import time
import os
import random
import json
from datetime import datetime

HITS_LOG = "logs/hits.log"
AEGIS_LOG = "logs/aegis.log"

def log_hit(ip, method, path, user_agent, intent="BENIGN"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    hit_entry = {
        "timestamp": timestamp,
        "ip": ip,
        "method": method,
        "path": path,
        "user_agent": user_agent,
        "intent": intent
    }
    
    with open(HITS_LOG, "a") as f:
        f.write(json.dumps(hit_entry) + "\n")

def analyze_intent(path, user_agent):
    # Basic rule-based intent analysis (Phase 2)
    # This will be replaced by SLM in Phase 4
    malicious_paths = ["/admin", "/wp-login.php", "/.env", "/config.php"]
    bot_agents = ["Python-urllib", "curl", "Wget", "Nmap"]
    
    if any(p in path for p in malicious_paths):
        return "MALICIOUS"
    if any(agent in user_agent for agent in bot_agents):
        return "BOT"
    return "BENIGN"

def run_monitor():
    if not os.path.exists("logs"):
        os.makedirs("logs")
    
    print(f"AegisShield Hit Monitor active. Tailing hits to {HITS_LOG}...")
    
    # In a real scenario, this would tail an external log file (e.g., Nginx access.log)
    # For now, we wait for hits to be logged by our simulator or other components
    while True:
        # This loop would normally process new lines from a log file
        time.sleep(1)

if __name__ == "__main__":
    try:
        run_monitor()
    except KeyboardInterrupt:
        print("\nMonitor stopped.")
