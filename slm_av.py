import os
import json
import argparse
import datetime
import shutil
from slm_inference import AegisSLM
from node_manager import get_nodes

STORY_LOG = "logs/story.log"
SIGNATURE_FILE = "logs/av_signatures.json"
FIX_LIST = "FIX_LIST.md"

def log_story(message):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    try:
        with open(STORY_LOG, "a") as f:
            f.write(f"[{timestamp}] 🦠 SLM AV: {message}\n")
    except: pass

def get_tech_stack(node):
    plan_path = os.path.join("logs", "deception_plan.json") # We use global logs for now based on current arch
    if os.path.exists(plan_path):
        try:
            with open(plan_path, "r") as f:
                return json.load(f).get("real_stack", "General Web")
        except: pass
    return "General Web"

def update_signatures():
    log_story("Initiating continuous Threat Intelligence signature generation...")
    nodes = get_nodes()
    if not nodes:
        log_story("No nodes found for signature generation.")
        return

    slm = AegisSLM()
    all_signatures = set()
    
    for node in nodes:
        stack = get_tech_stack(node)
        log_story(f"Generating signatures for node: {node} (Stack: {stack})")
        sigs = slm.generate_av_signatures(stack)
        all_signatures.update(sigs)
    
    # Save the consolidated signatures
    with open(SIGNATURE_FILE, "w") as f:
        json.dump(list(all_signatures), f, indent=4)
    
    log_story(f"Signatures updated successfully. {len(all_signatures)} research-standard IOCs generated.")

def quarantine_file(node, file_path, verdict):
    quarantine_dir = os.path.abspath("quarantine")
    if not os.path.exists(quarantine_dir):
        os.makedirs(quarantine_dir)
        
    filename = os.path.basename(file_path)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_filename = f"{filename}_{timestamp}.quarantined"
    quarantine_path = os.path.join(quarantine_dir, safe_filename)
    
    try:
        shutil.move(file_path, quarantine_path)
        log_story(f"🛡️ ACTIVE DEFENSE: File quarantined to {quarantine_path}")
        
        # Write forensic metadata
        metadata = {
            "original_node": node,
            "original_path": file_path,
            "quarantine_timestamp": timestamp,
            "slm_verdict": verdict,
            "status": "NEUTRALIZED"
        }
        meta_path = quarantine_path + "_metadata.json"
        with open(meta_path, "w") as f:
            json.dump(metadata, f, indent=4)
            
        log_to_fix_list(node, file_path, quarantine_path)
        return True
    except Exception as e:
        log_story(f"ERROR: Failed to quarantine {file_path}: {e}")
        return False

def log_to_fix_list(node, file_path, quarantine_path):
    entry = f"## 🚨 NEUTRALIZED MALWARE DETECTED\n**Node:** `{node}`\n**Original File:** `{file_path}`\n**Action Taken:** Automatically Quarantined. The SLM Semantic Engine definitively flagged this file as Malicious. It has been moved to `{quarantine_path}` and defanged to prevent execution.\n---\n"
    mode = "a" if os.path.exists(FIX_LIST) else "w"
    try:
        with open(FIX_LIST, mode) as f:
            if mode == "w":
                f.write("# 🛡️ AegisShield: Universal Fix List\n\n")
            f.write(entry)
    except: pass

def run_scan():
    if not os.path.exists(SIGNATURE_FILE):
        log_story("Warning: No signatures found. Updating signatures first...")
        update_signatures()
        
    try:
        with open(SIGNATURE_FILE, "r") as f:
            signatures = json.load(f)
    except:
        log_story("Error reading signatures. Scan aborted.")
        return

    nodes = get_nodes()
    if not nodes: return
    
    log_story(f"Starting real-time semantic AV scan across {len(nodes)} nodes using {len(signatures)} signatures.")
    slm = AegisSLM()

    malware_found = 0

    for node in nodes:
        if not os.path.exists(node): continue
        if os.path.abspath(node) == os.path.abspath(os.path.dirname(__file__)):
            continue # Don't aggressively scan Aegis core to prevent self-deletion

        for root, dirs, files in os.walk(node):
            if any(exc in root for exc in [".git", "venv", "node_modules", "digital_twin"]):
                continue
                
            for f in files:
                file_path = os.path.join(root, f)
                
                # 1. Fast match against signatures (Heuristics)
                suspicious = False
                for sig in signatures:
                    if sig in f: # Match filename or extension
                        suspicious = True
                        break
                        
                # Read content if filename matched OR if it's a script/text file (we check inside)
                if not suspicious and f.endswith(('.php', '.js', '.py', '.sh', '.bash', '.pl')):
                    try:
                        with open(file_path, "r", errors="ignore") as file_content:
                            content = file_content.read()
                            for sig in signatures:
                                if sig in content: # Hex or snippet match
                                    suspicious = True
                                    break
                    except: pass
                
                # 2. Deep Semantic Verification
                if suspicious:
                    log_story(f"Heuristics triggered for: {file_path}. Initiating Deep Semantic Inspection...")
                    try:
                        with open(file_path, "r", errors="ignore") as fc:
                            content = fc.read()
                        
                        verdict = slm.analyze_suspicious_file(content)
                        if verdict == "MALICIOUS":
                            log_story(f"!!! MALWARE CONFIRMED !!! Path: {file_path}")
                            quarantined = quarantine_file(node, file_path, verdict)
                            if quarantined:
                                malware_found += 1
                        else:
                            log_story(f"False positive resolved globally for: {file_path}")
                    except: pass

    log_story(f"Real-time scan complete. Found {malware_found} confirmed malicious artifacts.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="AegisShield SLM Anti-Virus")
    parser.add_argument("--update-signatures", action="store_true", help="Generate new IOCs based on tech stack")
    parser.add_argument("--scan", action="store_true", help="Run active semantic scan across nodes")
    
    args = parser.parse_args()
    
    if args.update_signatures:
        update_signatures()
    elif args.scan:
        run_scan()
    else:
        # Default behavior for cron/daemon if no args passed: Run signature generation occasionally, but mainly scan
        run_scan()
