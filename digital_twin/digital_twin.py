import os
import shutil
import subprocess
from datetime import datetime

TWIN_DIR = "digital_twin"
LOG_FILE = "logs/aegis.log"

def log_message(level, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] [{level}] {message}\n")

def sync_twin(root_dir):
    if not os.path.exists(TWIN_DIR):
        os.makedirs(TWIN_DIR)
    
    log_message("INFO", f"Syncing Digital Twin from {root_dir}")
    # Simple copy for now, excluding some dirs
    exclude_dirs = {".git", "logs", "digital_twin", "tests", ".pytest_cache", "__pycache__", ".venv"}
    
    for item in os.listdir(root_dir):
        s = os.path.join(root_dir, item)
        d = os.path.join(TWIN_DIR, item)
        if item in exclude_dirs:
            continue
        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
    
    log_message("INFO", "Digital Twin sync complete.")

def run_safe_attack(attack_type):
    log_message("ART", f"Triggering Safe Attack Simulation: {attack_type}")
    
    if attack_type == "REMOVAL_ATTACK":
        # Simulate an attacker trying to delete a file in the twin
        target = os.path.join(TWIN_DIR, "shield.sh")
        if os.path.exists(target):
            os.remove(target)
            return True, "Simulated attacker deleted shield.sh in Digital Twin."
    
    elif attack_type == "CONFIG_EXPOSURE":
        # Simulate an attacker creating a .env file
        target = os.path.join(TWIN_DIR, ".env")
        with open(target, "w") as f:
            f.write("SECRET_KEY=12345")
        return True, "Simulated attacker created .env in Digital Twin."

    return False, "Unknown attack type."

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "sync":
            sync_twin(".")
        elif sys.argv[1] == "attack":
            success, msg = run_safe_attack(sys.argv[2] if len(sys.argv) > 2 else "REMOVAL_ATTACK")
            print(msg)
