import os
import time
from datetime import datetime
import json

LOG_DIR = "logs"
TWIN_DIR = "digital_twin"
QUARANTINE_DIR = "quarantine"
TRACKER_FILE = "logs/quarantine_tracker.json"
MAX_LOG_SIZE_MB = 50 # Total log folder limit
STORY_LOG = "logs/story.log"
MAX_QUARANTINE_DAYS = 30

def log_story(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    try:
        with open(STORY_LOG, "a") as f:
            f.write(f"[{timestamp}] 🧹 Garbage Collector: {message}\n")
    except: pass

def get_dir_size(path):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
            elif entry.is_dir():
                total += get_dir_size(entry.path)
    return total

def rotate_logs():
    if not os.path.exists(LOG_DIR): return
    
    current_size = get_dir_size(LOG_DIR) / (1024 * 1024)
    
    if current_size > MAX_LOG_SIZE_MB:
        log_story(f"Log directory reached {current_size:.2f}MB. Initiating purge...")
        
        # 1. Clean up oldest logs
        # We'll truncate all .log files to the last 1000 lines
        for f in os.listdir(LOG_DIR):
            if f.endswith(".log"):
                file_path = os.path.join(LOG_DIR, f)
                try:
                    with open(file_path, "r") as log_file:
                        lines = log_file.readlines()
                    
                    if len(lines) > 1000:
                        with open(file_path, "w") as log_file:
                            log_file.writelines(lines[-1000:]) # Keep only last 1000 lines
                except: pass
        
        log_story("Cleanup complete. Logs truncated to maintain storage balance.")

def clean_twin():
    """Ensure the Digital Twin doesn't contain massive temp files."""
    if os.path.exists(TWIN_DIR):
        # Scan for .pyc, __pycache__, or massive temp files in twin
        for root, dirs, files in os.walk(TWIN_DIR):
            for f in files:
                if f.endswith(".pyc") or f.startswith("."):
                    try: os.remove(os.path.join(root, f))
                    except: pass

def clean_quarantine():
    """Removes quarantined files that have exceeded the 30-day retention policy."""
    if not os.path.exists(QUARANTINE_DIR):
        return
    
    now = time.time()
    deleted_count = 0
    
    for filename in os.listdir(QUARANTINE_DIR):
        filepath = os.path.join(QUARANTINE_DIR, filename)
        if os.path.isfile(filepath):
            file_mod_time = os.stat(filepath).st_mtime
            age_days = (now - file_mod_time) / (24 * 3600)
            
            if age_days > MAX_QUARANTINE_DAYS:
                try:
                    os.remove(filepath)
                    deleted_count += 1
                except:
                    pass
                    
    if deleted_count > 0:
        log_story(f"Purged {deleted_count} expired quarantined file(s).")
    
    # Update daily tracking metric
    today_str = datetime.now().strftime("%Y-%m-%d")
    tracker_data = {"date": today_str, "deleted_today": 0}
    
    if os.path.exists(TRACKER_FILE):
        try:
            with open(TRACKER_FILE, "r") as f:
                data = json.load(f)
                if data.get("date") == today_str:
                    tracker_data = data
        except:
            pass
            
    tracker_data["deleted_today"] += deleted_count
    
    try:
        with open(TRACKER_FILE, "w") as f:
            json.dump(tracker_data, f)
    except:
        pass

if __name__ == "__main__":
    rotate_logs()
    clean_twin()
    clean_quarantine()
