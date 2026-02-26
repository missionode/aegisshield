import socket
import threading
import os
import json
import time
import subprocess
from datetime import datetime

DECEPTION_PLAN = "logs/deception_plan.json"
STORY_LOG = "logs/story.log"
HITS_LOG = "logs/hits.log"
TARPIT_DELAY = 15 # Seconds to hold the connection open

# Expanded list for Port Spoofing simulation
SPOOF_PORTS = [21, 22, 23, 25, 53, 110, 143, 443, 445, 3306, 3389, 5900, 8080]

def log_story(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(STORY_LOG, "a") as f:
        f.write(f"[{timestamp}] 🕸️ TARPIT: {message}\n")

def log_hit(ip, method, path, intent):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f'{{"timestamp": "{timestamp}", "ip": "{ip}", "method": "{method}", "path": "{path}", "user_agent": "Scanner", "intent": "{intent}"}}\n'
    with open(HITS_LOG, "a") as f:
        f.write(entry)

def load_plan():
    if os.path.exists(DECEPTION_PLAN):
        with open(DECEPTION_PLAN, "r") as f:
            return json.load(f)
    return {"whitelist": ["127.0.0.1"]}

def handle_tarpit(client_sock, port, whitelist):
    """The Tarpit: Hold the connection open to waste attacker resources."""
    try:
        ip = client_sock.getpeername()[0]
        if ip in whitelist:
            client_sock.close()
            return

        log_story(f"Attacker {ip} caught in Tarpit on Port {port}. Holding for {TARPIT_DELAY}s...")
        log_hit(ip, "TCP", f"PORT_{port}", "WARNING/TARPIT_ENGAGED")
        
        # Slowly send garbage data to keep them interested but frustrated
        for i in range(TARPIT_DELAY):
            if i % 5 == 0:
                try:
                    client_sock.send(b"\0") # Send a single null byte
                except:
                    break # Connection closed by attacker
            time.sleep(1)
            
        log_story(f"Tarpit released for {ip} on Port {port}.")
    except Exception:
        pass
    finally:
        try:
            client_sock.close()
        except:
            pass

def start_listener(port, whitelist):
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(('0.0.0.0', port))
        server.listen(10)
        while True:
            client, addr = server.accept()
            threading.Thread(target=handle_tarpit, args=(client, port, whitelist), daemon=True).start()
    except Exception:
        pass # Port already in use by real app

if __name__ == "__main__":
    plan = load_plan()
    whitelist = plan.get("whitelist", ["127.0.0.1"])
    
    print(f"AegisShield Network Tarpit Active.")
    log_story(f"Port Spoofing Active. Simulating open services on {len(SPOOF_PORTS)} ports.")
    
    threads = []
    for p in SPOOF_PORTS:
        t = threading.Thread(target=start_listener, args=(p, whitelist), daemon=True)
        t.start()
        threads.append(t)
    
    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("Tarpit Module stopped.")
