import os
import time
from datetime import datetime

LOG_DIR = "logs"
TWIN_DIR = "digital_twin"
MAX_LOG_SIZE_MB = 50 # Total log folder limit
STORY_LOG = "logs/story.log"

def log_story(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    try:
        with open(STORY_LOG, "a") as f:
            f.write(f"[{timestamp}] 🧹 Garbage Collector: {message}
")
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

if __name__ == "__main__":
    rotate_logs()
    clean_twin()
