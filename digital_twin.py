import os
import shutil
import subprocess
from datetime import datetime

TWIN_DIR = "digital_twin"
LOG_FILE = "logs/aegis.log"
STORY_LOG = "logs/story.log"

def log_story(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(STORY_LOG, "a") as f:
        f.write(f"[{timestamp}] {message}\n")

def log_message(level, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if level in ["INFO", "ART"]:
        log_story(f"🔬 {message}")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] [{level}] {message}\n")

def sync_twin(root_dir):
    if not os.path.exists(TWIN_DIR):
        os.makedirs(TWIN_DIR)
    
    log_message("INFO", f"Syncing Digital Twin from {root_dir}")
    exclude_dirs = {".git", "logs", "digital_twin", "tests", ".pytest_cache", "__pycache__", ".venv", "venv", "node_modules"}
    
    def ignore_files(dir_name, contents):
        return [c for c in contents if c in exclude_dirs]

    for item in os.listdir(root_dir):
        if item in exclude_dirs:
            continue
        s = os.path.join(root_dir, item)
        d = os.path.join(TWIN_DIR, item)
        try:
            if os.path.isdir(s):
                if os.path.exists(d):
                    shutil.rmtree(d)
                shutil.copytree(s, d, ignore=ignore_files)
            else:
                shutil.copy2(s, d)
        except Exception:
            pass
    
    log_message("INFO", "Digital Twin sync complete.")

def run_real_scan(root_dir):
    findings = []
    log_message("ART", f"Starting LIVE vulnerability scan on {root_dir}")
    
    # 1. Exposed .env
    env_path = os.path.join(root_dir, ".env")
    if os.path.exists(env_path):
        mode = oct(os.stat(env_path).st_mode & 0o777)
        findings.append({
            "type": "EXPOSED_ENV", 
            "path": env_path, 
            "details": f"Permissions: {mode}",
            "snippet": "N/A (Sensitive File)",
            "line": 0,
            "block": "N/A"
        })
    
    # 2. Extract previously hardened vulnerabilities from FIX_LIST
    hardened_snippets = set()
    fix_lists = ["../FIX_LIST.md", "FIX_LIST.md"]
    for fl_path in fix_lists:
        try:
            full_path = os.path.join(root_dir, fl_path)
            if os.path.exists(full_path):
                with open(full_path, "r") as f:
                    for line in f:
                        # Format: | [X] | Vulnerability | `path` | `snippet` | Action | Context |
                        if "| [X] |" in line:
                            parts = [p.strip() for p in line.split("|")]
                            if len(parts) >= 5:
                                # Clean the ticks around the snippet
                                snippet = parts[4].replace("`", "").strip()
                                hardened_snippets.add(snippet)
        except Exception:
            pass
            
    if hardened_snippets:
        log_message("INFO", f"Optimization: Loaded {len(hardened_snippets)} hardened snippets to skip.")
    
    # 3. Recursive scan
    exclude_patterns = ["digital_twin", "logs", ".git", ".venv", "venv", "node_modules", "site-packages", "__pycache__"]
    
    for root, dirs, files in os.walk(root_dir):
        if any(exc in root for exc in exclude_patterns):
            continue
            
        for f in files:
            file_path = os.path.join(root, f)
            
            # Logic Flaws: Contextual Analysis
            if f.endswith((".py", ".js", ".php", ".sh")):
                try:
                    with open(file_path, "r", errors="ignore") as code_file:
                        lines = code_file.readlines()
                        logic_risks = {
                            "eval(": "Code injection risk.",
                            "shell=True": "Command injection risk.",
                            "os.system(": "Insecure execution risk.",
                            "apiKey =": "Hardcoded secret risk."
                        }
                        for i, line in enumerate(lines):
                            for pattern, desc in logic_risks.items():
                                if pattern in line:
                                    # Extract context block (5 lines around)
                                    start = max(0, i - 5)
                                    end = min(len(lines), i + 5)
                                    context_block = "".join(lines[start:end])
                                    
                                    clean_snippet = line.strip()
                                    if clean_snippet in hardened_snippets:
                                        # Optimization: Skip already verified fixes
                                        continue
                                        
                                    findings.append({
                                        "type": "LOGIC_FLAW",
                                        "path": file_path,
                                        "details": desc,
                                        "line": i + 1,
                                        "snippet": clean_snippet,
                                        "block": context_block # New for Phase 19
                                    })
                except Exception:
                    pass

    return findings

if __name__ == "__main__":
    import sys
    import json
    if len(sys.argv) > 1:
        if sys.argv[1] == "sync":
            target_root = sys.argv[2] if len(sys.argv) > 2 else ".."
            sync_twin(target_root)
        elif sys.argv[1] == "scan":
            target_root = sys.argv[2] if len(sys.argv) > 2 else ".."
            findings = run_real_scan(target_root)
            print(json.dumps(findings))
