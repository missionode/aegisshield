import os
import json
import shutil
import datetime
from slm_inference import AegisSLM
from node_manager import get_nodes

STORY_LOG = "logs/story.log"

def log_story(message):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    try:
        with open(STORY_LOG, "a") as f:
            f.write(f"[{timestamp}] 🧹 SLM Scavenger: {message}\n")
    except: pass

def run_scavenger():
    nodes = get_nodes()
    if not nodes:
        log_story("No nodes to scavenge.")
        return

    log_story(f"Starting scavenge cycle for {len(nodes)} nodes.")
    
    # Pre-Scavenge: Groom FIX_LIST.md globally
    try:
        fix_list_path = "../FIX_LIST.md"
        if os.path.exists(fix_list_path):
            log_story("Grooming FIX_LIST.md for stale/failed patch attempts...")
            with open(fix_list_path, "r") as f:
                lines = f.readlines()
            # Remove lines that contain 'PATCH_FAILED' because they will never be picked up by the doctor again
            # Assuming these will be handled by humans or simply cleaned out if too old.
            new_lines = [l for l in lines if "PATCH_FAILED" not in l]
            if len(new_lines) < len(lines):
                 with open(fix_list_path, "w") as f:
                      f.writelines(new_lines)
                 log_story(f"Removed {len(lines) - len(new_lines)} stale PATCH_FAILED entries from FIX_LIST.")
    except Exception as e:
        log_story(f"Grooming FIX_LIST failed: {e}")

    slm = AegisSLM()

    total_freed = 0
    files_deleted = 0
    dirs_deleted = 0

    for node in nodes:
        if not os.path.exists(node): continue
        
        # 1. Determine Tech Stack (try from deception_plan.json or default to generic)
        tech_stack = "Unknown"
        plan_path = "logs/deception_plan.json"
        if os.path.exists(plan_path):
            try:
                with open(plan_path, "r") as f:
                    plan = json.load(f)
                    tech_stack = plan.get("real_stack", "Unknown")
            except: pass
            
        # 2. Ask SLM for Junk Patterns
        log_story(f"Analyzing junk patterns for {node} (Stack: {tech_stack})...")
        patterns = slm.get_junk_patterns(tech_stack)
        log_story(f"SLM suggested unsafe patterns: {patterns}")
        
        # 3. Clean up matched junk (Safe Delete)
        # Be careful not to delete important files. We will only delete if it matches the pattern
        # and it's within the node directory (but not AegisShield itself)
        
        if os.path.abspath(node) == os.path.abspath(os.path.dirname(__file__)):
            # Don't scavenge AegisShield's own root aggressively
            continue

        for root, dirs, files in os.walk(node):
            # Skip safe/important directories
            if any(exc in root for exc in [".git", "venv", "digital_twin"]):
                continue

            # Check Directories
            for d in list(dirs):
                for p in patterns:
                    if p.replace("/", "") == d or d.endswith(p):
                        target_dir = os.path.join(root, d)
                        try:
                            size = sum(os.path.getsize(os.path.join(r, f)) for r, ds, fs in os.walk(target_dir) for f in fs)
                            shutil.rmtree(target_dir)
                            total_freed += size
                            dirs_deleted += 1
                            log_story(f"Deleted directory: {target_dir}")
                            dirs.remove(d) # Prevent descending into deleted dir
                            break # Found pattern
                        except: pass

            # Check Files
            for f in files:
                for p in patterns:
                    if f.endswith(p) or f == p:
                        target_file = os.path.join(root, f)
                        try:
                            size = os.path.getsize(target_file)
                            os.remove(target_file)
                            total_freed += size
                            files_deleted += 1
                        except: pass

    freed_mb = total_freed / (1024 * 1024)
    log_story(f"Scavenge complete. Freed {freed_mb:.2f}MB ({files_deleted} files, {dirs_deleted} directories deleted).")

if __name__ == "__main__":
    run_scavenger()
