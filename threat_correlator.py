import json
import os
from datetime import datetime

FINGERPRINT_FILE = "logs/system_fingerprint.json"
STORY_LOG = "logs/story.log"

def log_story(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(STORY_LOG, "a") as f:
        f.write(f"[{timestamp}] 🎯 Correlation: {message}
")

def correlate_threat(threat_title, threat_desc):
    """Compares a new threat against the known system stack."""
    if not os.path.exists(FINGERPRINT_FILE):
        return False, "Fingerprint not found."

    with open(FINGERPRINT_FILE, "r") as f:
        fingerprint = json.load(f)
    
    stack_info = fingerprint.get("slm_determination", {})
    real_stack = stack_info.get("tech_stack", "Unknown")
    
    log_story(f"Analyzing relevance of new threat to your {real_stack} stack...")

    # Define simple relevance keywords based on stack
    relevance_map = {
        "Django": ["python", "django", "sql", "pip"],
        "Python": ["python", "pip", "rce"],
        "Node.js": ["node", "npm", "javascript", "express"],
        "PHP": ["php", "laravel", "composer", "wordpress"],
        "Go": ["go", "golang"],
        "Java": ["java", "spring", "log4j", "maven"]
    }

    keywords = []
    for stack, k in relevance_map.items():
        if stack.lower() in real_stack.lower():
            keywords.extend(k)

    content = (threat_title + " " + threat_desc).lower()
    
    # Correlation Check
    is_relevant = any(k in content for k in keywords)
    
    if is_relevant:
        log_story(f"🚨 CRITICAL CORRELATION: This threat targets your {real_stack} stack! I am prioritizing a deeper scan.")
        # Trigger an immediate analysis in the background
        import subprocess
        subprocess.Popen(["python3", "slm_engine.py", ".."], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True, "Relevant"
    else:
        log_story(f"Informational: New threat detected but appears low-risk for your current stack.")
        return False, "Not relevant"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        correlate_threat(sys.argv[1], sys.argv[2])
