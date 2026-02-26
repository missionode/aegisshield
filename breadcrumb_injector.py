import os
import random
import string
import json
from datetime import datetime

STORY_LOG = "logs/story.log"
BREADCRUMB_DB = "logs/active_breadcrumbs.json"

def log_story(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(STORY_LOG, "a") as f:
        f.write(f"[{timestamp}] 🍞 BREADCRUMB: {message}\n")

def generate_token(length=24):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def inject_breadcrumbs(root_dir):
    """Injects fake 'Canary' comments into project source files."""
    log_story(f"Starting Breadcrumb Injection in {root_dir}...")
    
    breadcrumbs = []
    # Targeted files for injection
    target_exts = (".py", ".js", ".sh", ".yaml", ".yml", ".env")
    exclude_dirs = ["venv", ".venv", "node_modules", ".git", "digital_twin", "logs"]
    
    for root, dirs, files in os.walk(root_dir):
        if any(exc in root for exc in exclude_dirs): continue
        
        for f in files:
            if f.endswith(target_exts):
                file_path = os.path.join(root, f)
                try:
                    # Create a unique token for this file
                    token_id = generate_token(12)
                    fake_secret = f"aegis_sec_{generate_token(20)}"
                    
                    comment_style = "#"
                    if f.endswith(".js"): comment_style = "//"
                    
                    breadcrumb_line = f"
{comment_style} DEBUG_TOKEN: {token_id} | INTERNAL_KEY: {fake_secret}
"
                    
                    with open(file_path, "a") as code_file:
                        code_file.write(breadcrumb_line)
                    
                    breadcrumbs.append({
                        "file": file_path,
                        "token": token_id,
                        "secret": fake_secret,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
                except: pass

    # Store for monitor to watch
    with open(BREADCRUMB_DB, "w") as db:
        json.dump(breadcrumbs, db, indent=4)
        
    log_story(f"Successfully injected {len(breadcrumbs)} Breadcrumbs across the root.")
    return breadcrumbs

if __name__ == "__main__":
    import sys
    inject_breadcrumbs(sys.argv[1] if len(sys.argv) > 1 else "..")
