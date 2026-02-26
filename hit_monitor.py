import time
import os
import json
import subprocess
import threading
from datetime import datetime
from collections import defaultdict
from slm_inference import AegisSLM

HITS_LOG = "logs/hits.log"
WEB_ACCESS_LOG = "logs/web_access.log"
STORY_LOG = "logs/story.log"

# Security Thresholds
BRUTE_FORCE_THRESHOLD = 5 
ip_hit_history = defaultdict(list)
seen_active_conns = set()
traffic_batch = [] # Buffer for SLM Second Opinion

def log_story(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(STORY_LOG, "a") as f:
        f.write(f"[{timestamp}] 📡 SOC: {message}\n")

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
    
    # Store in batch for AI review if it's not a known critical hit
    if intent in ["BENIGN", "BOT", "PROBE/SENSITIVE_PATH"]:
        traffic_batch.append(f"{ip} {method} {path}")
        if len(traffic_batch) > 50: traffic_batch.pop(0)

    with open(HITS_LOG, "a") as f:
        f.write(json.dumps(hit_entry) + "\n")

    if "MALICIOUS" in intent or "CRITICAL" in intent:
        log_story(f"Threat Detected: {intent} from {ip} on {path}")
    elif intent == "ACTIVE_CONN":
        log_story(f"New Active Connection established: {ip}")

def analyze_intent(ip, method, path, user_agent):
    now = time.time()
    
    # Rule-based (Fast Path)
    if os.path.exists("logs/active_breadcrumbs.json"):
        try:
            with open("logs/active_breadcrumbs.json", "r") as f:
                for b in json.load(f):
                    if b["token"] in path or b["token"] in user_agent:
                        return "CRITICAL/BREADCRUMB_TRIGGER"
        except: pass

    sql_payloads = ["select", "union", "drop", "insert", "update", "--", "order by"]
    if any(payload in path.lower() for payload in sql_payloads):
        return "MALICIOUS/SQL_INJECTION"

    malicious_paths = ["/admin", "/login", "/wp-login.php", "/config.php", "/.env"]
    if any(p in path for p in malicious_paths):
        ip_hit_history[ip] = [t for t in ip_hit_history[ip] if now - t < 60]
        ip_hit_history[ip].append(now)
        if len(ip_hit_history[ip]) >= BRUTE_FORCE_THRESHOLD:
            return "MALICIOUS/BRUTE_FORCE"
        return "PROBE/SENSITIVE_PATH"

    bot_agents = ["Python-urllib", "curl", "Wget", "Nmap", "sqlmap"]
    if any(agent in user_agent for agent in bot_agents):
        return "BOT"

    return "BENIGN"

def slm_behavioral_review():
    """Background thread: Periodically asks SLM for a 'Second Opinion' on traffic patterns."""
    slm = None
    while True:
        time.sleep(300) # Review every 5 minutes
        if len(traffic_batch) < 5: continue
        
        try:
            if slm is None: slm = AegisSLM()
            
            # Format batch for prompt
            batch_str = "\n".join(traffic_batch[-20:]) # Last 20 hits
            log_story("AI is performing a behavioral review of recent traffic batch...")
            
            analysis = slm.classify_traffic(batch_str)
            log_story(f"AI Behavioral Report: {analysis}")
            
            # Reset batch after review to watch for new patterns
            traffic_batch.clear()
        except Exception as e:
            pass

def active_network_monitor():
    """Scans established TCP connections every 5 seconds."""
    global seen_active_conns
    while True:
        try:
            result = subprocess.run(["lsof", "-iTCP", "-sTCP:ESTABLISHED", "-n", "-P"], capture_output=True, text=True)
            lines = result.stdout.splitlines()
            current_ips = set()
            for line in lines[1:]:
                parts = line.split()
                if len(parts) > 8:
                    conn = parts[8]
                    if "->" in conn:
                        remote_part = conn.split("->")[1]
                        # Handle IPv6 brackets and split port from last colon
                        remote_ip = remote_part.rsplit(":", 1)[0].replace("[", "").replace("]", "")
                        
                        if remote_ip != "127.0.0.1" and "::1" not in remote_ip:
                            current_ips.add(remote_ip)
                            if remote_ip not in seen_active_conns:
                                log_hit(remote_ip, "TCP", "RAW_CONNECTION", "System-Stack", "ACTIVE_CONN")
            seen_active_conns = current_ips
        except: pass
        time.sleep(5)

def tail_web_log():
    if not os.path.exists(WEB_ACCESS_LOG):
        open(WEB_ACCESS_LOG, 'a').close()
    with open(WEB_ACCESS_LOG, 'r') as f:
        f.seek(0, 2)
        while True:
            line = f.readline()
            if not line:
                time.sleep(0.1)
                continue
            try:
                parts = line.split()
                if len(parts) > 6:
                    ip = parts[0]
                    method = parts[5].strip('"')
                    path = parts[6]
                    user_agent = line.split('"')[-2] if '"' in line else "Web-Browser"
                    intent = analyze_intent(ip, method, path, user_agent)
                    log_hit(ip, method, path, user_agent, intent)
            except: pass

if __name__ == "__main__":
    if not os.path.exists("logs"): os.makedirs("logs")
    print("AegisShield SOC starting (Intelligence Mode)...")
    
    threading.Thread(target=active_network_monitor, daemon=True).start()
    threading.Thread(target=slm_behavioral_review, daemon=True).start()
    tail_web_log()
