import os
import sys
import re
import json
import subprocess
import tempfile
import shutil
from datetime import datetime
from slm_inference import AegisSLM
from digital_twin import sync_twin, TWIN_DIR
from node_manager import get_nodes

# Authoritative location for the multi-node fix list
FIX_LIST_PATH = "../FIX_LIST.md"
LOCAL_FIX_LIST_PATH = "FIX_LIST.md"
AEGIS_LOG = "logs/aegis.log"
STORY_LOG = "logs/story.log"
PATCH_DIR = "logs/patches"

def log_story(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(STORY_LOG, "a") as f:
        f.write(f"[{timestamp}] 👨‍⚕️ SLM Doctor: {message}\n")
    print(f"[{timestamp}] 👨‍⚕️ SLM Doctor: {message}")

def get_syntax_checker(file_path):
    """Dynamically determines the syntax checker and arguments based on file extension."""
    ext = os.path.splitext(file_path)[1].lower()
    if ext == ".py":
        return ["python3", "-m", "py_compile", file_path]
    elif ext == ".php":
        return ["php", "-l", file_path]
    elif ext == ".sh":
        return ["bash", "-n", file_path]
    elif ext == ".js":
        return ["node", "-c", file_path]
    else:
        # Fallback for unknown tech stacks
        return []

def find_fix_list():
    """Locates the active FIX_LIST.md by checking parent and local folders."""
    if os.path.exists(FIX_LIST_PATH):
        return FIX_LIST_PATH
    if os.path.exists(LOCAL_FIX_LIST_PATH):
        return LOCAL_FIX_LIST_PATH
    return None

def run_doctor():
    active_fix_list = find_fix_list()
    if not active_fix_list:
        log_story("FIX_LIST.md not found in parent or local directory. Operation skipped.")
        return

    log_story(f"Waking up. Scanning {active_fix_list} for actionable items...")
    
    with open(active_fix_list, "r") as f:
        lines = f.readlines()

    target_idx = -1
    target_data = {}
    nodes = get_nodes()

    for i, line in enumerate(lines):
        if line.startswith("| [ ] |"):
            # Skip if it's already marked as PATCH_FAILED
            if "PATCH_FAILED" in line:
                continue

            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 5:
                # Basic validation to see if it's a code finding with a path
                vuln_type_raw = parts[2]
                loc_col = parts[3]
                
                # Match the absolute path from the Location column
                match = re.search(r'`(?:\[.*?\]\s*)?(/.*?)(?:\s*\(Line.*?\))?`', loc_col)
                if match:
                    actual_path = match.group(1).strip()
                    if os.path.exists(actual_path) and os.path.isfile(actual_path):
                        # Determine which node this file belongs to
                        node_root = None
                        for node in nodes:
                            if actual_path.startswith(node):
                                node_root = node
                                break
                        
                        if not node_root:
                            # Fallback: check if it's in the aegisshield directory itself
                            shield_root = os.path.dirname(os.path.abspath(__file__))
                            if actual_path.startswith(shield_root):
                                node_root = shield_root
                        
                        if node_root:
                            snip_match = re.search(r'`(?:\[.*?\]\s*)?(.*?)`', parts[4])
                            actual_snippet = snip_match.group(1).strip() if snip_match else parts[4].replace("`", "")

                            target_idx = i
                            target_data = {
                                "line_raw": line,
                                "path": actual_path,
                                "node_root": node_root,
                                "snippet": actual_snippet,
                                "vuln": parts[2]
                            }
                            break
                    
    if target_idx == -1:
        log_story("No actionable or un-failed items found. Going back to sleep.")
        return

    log_story(f"Identified item to patch: {target_data['path']} (Node: {target_data['node_root']})")
    log_story(f"Snippet: '{target_data['snippet'][:30]}...'")

    # 1. Sync Twin for the identified node root
    sync_twin(target_data['node_root'])
    
    # Calculate path in Twin
    rel_path = os.path.relpath(target_data['path'], start=target_data['node_root'])
    twin_path = os.path.join(TWIN_DIR, rel_path)

    if not os.path.exists(twin_path):
         log_story(f"Twin path {twin_path} does not exist. Aborting patch.")
         mark_failed(lines, target_idx, "Twin file not found", active_fix_list)
         return

    # 2. Intel Gathering via SLM
    slm = AegisSLM()
    log_story("Consulting SLM for a secure rewrite...")
    try:
        with open(twin_path, "r") as f:
            original_code = f.read()

        # Find the block around the snippet
        lines_of_code = original_code.split('\n')
        snip_line_idx = -1
        for j, ln in enumerate(lines_of_code):
            if target_data['snippet'] in ln:
                snip_line_idx = j
                break
        
        if snip_line_idx == -1:
             raise ValueError("Snippet not found in original file.")
             
        start = max(0, snip_line_idx - 3)
        end = min(len(lines_of_code), snip_line_idx + 3)
        context_block = '\n'.join(lines_of_code[start:end])

        secure_code = slm.suggest_code_fix(context_block, "vulnerability")
        if not secure_code or len(secure_code) < 5:
             raise ValueError("SLM generated empty or invalid response.")

        log_story(f"SLM provided secure snippet. Applying to Twin...")
        
        new_code = original_code.replace(context_block, secure_code)
        if new_code == original_code:
             # Try simple replace
             new_code = original_code.replace(target_data['snippet'], secure_code)
             if new_code == original_code:
                 raise ValueError("Could not neatly apply SLM patch to source text.")

        with open(twin_path, "w") as f:
            f.write(new_code)

    except Exception as e:
        log_story(f"Failed to generate/apply patch: {str(e)}")
        mark_failed(lines, target_idx, str(e), active_fix_list)
        return

    # 3. Create Git Patch via diff
    os.makedirs(PATCH_DIR, exist_ok=True)
    patch_filename = os.path.join(PATCH_DIR, f"patch_{datetime.now().strftime('%Y%m%d%H%M%S')}.patch")
    log_story(f"Generating Git Patch: {patch_filename}")
    try:
        with open(patch_filename, "w") as patch_file:
             subprocess.run(["diff", "-u", target_data['path'], twin_path], stdout=patch_file)
    except Exception as e:
        log_story(f"Warning: Could not create git patch: {str(e)}")

    # 4. Tech-Stack Error Scanning
    checker_cmd = get_syntax_checker(twin_path)
    if checker_cmd:
        log_story(f"Running syntax validation: {' '.join(checker_cmd)}")
        result = subprocess.run(checker_cmd, capture_output=True, text=True)
        if result.returncode != 0:
            err_msg = result.stderr.strip() or result.stdout.strip()
            log_story(f"Syntax validation FAILED: {err_msg[:100]}")
            mark_failed(lines, target_idx, f"Syntax Error: {err_msg[:50]}", active_fix_list)
            return
    else:
        log_story(f"No syntax checker assigned for {os.path.splitext(twin_path)[1]}. Trusting SLM implicitly.")

    # 5. Success -> Apply to Parent
    log_story(f"Tests passed. Deploying fix to parent folder: {target_data['path']}")
    try:
        shutil.copy2(twin_path, target_data['path'])
    except Exception as e:
        log_story(f"Failed to apply to parent: {str(e)}")
        mark_failed(lines, target_idx, f"Apply Failed: {str(e)}", active_fix_list)
        return

    # 6. Remove from FIX_LIST
    log_story(f"Cleaning up {active_fix_list}...")
    del lines[target_idx]
    with open(active_fix_list, "w") as f:
        f.writelines(lines)
    
    log_story("Operation successfully completed.")


def mark_failed(lines, idx, reason, fix_list_path):
    """Updates the FIX_LIST.md item to indicate failure."""
    old_line = lines[idx]
    # Remove leading/trailing pipes and split
    content = old_line.strip().strip("|")
    parts = [p.strip() for p in content.split("|")]
    if len(parts) >= 5:
        timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
        # column 5 is "Recommended Action" (index 4 if we stripped pipes)
        # But let's stay consistent with the table: 
        # | Status | Vuln | Loc | Snip | Action | Context |
        # indices: 0:Status, 1:Vuln, 2:Loc, 3:Snip, 4:Action, 5:Context
        if len(parts) > 4:
            parts[4] = f"{timestamp} PATCH_FAILED: {reason}"
        
        new_line = "| " + " | ".join(parts) + " |\n"
        lines[idx] = new_line
        with open(fix_list_path, "w") as f:
            f.writelines(lines)

if __name__ == "__main__":
    run_doctor()
