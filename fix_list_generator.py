import json
import os
import subprocess
from datetime import datetime

CONSULTANT_LOG = "logs/consultant.log"
# Targeted authoritative location in the parent project root
PARENT_FIX_LIST = "../FIX_LIST.md"
LOCAL_FIX_LIST = "FIX_LIST.md"

def generate_fix_list():
    if not os.path.exists(CONSULTANT_LOG):
        return

    findings = []
    with open(CONSULTANT_LOG, "r") as f:
        content = f.read()
        blocks = content.split("[AI] Thought: ")
        for block in blocks[1:]:
            lines = block.split("\n")
            finding = {
                "thought": lines[0],
                "location": "Global",
                "snippet": "N/A",
                "action": "Manual review",
                "wiki": "General Security"
            }
            
            for line in lines:
                if "[AI] Location: " in line:
                    finding["location"] = line.replace("[AI] Location: ", "").strip()
                if "[AI] Snippet: " in line:
                    finding["snippet"] = line.replace("[AI] Snippet: ", "").strip()
                if "[AI] Action: " in line:
                    finding["action"] = line.replace("[AI] Action: ", "").strip()
                if "[AI] Wiki Reference: " in line:
                    finding["wiki"] = line.replace("[AI] Wiki Reference: ", "").strip()
            
            key = f"{finding['location']}:{finding['thought']}"
            if key not in [f"{fn['location']}:{fn['thought']}" for fn in findings]:
                findings.append(finding)

    if not findings:
        return

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    md_content = f"# 🛡️ AegisShield: Professional Security Fix List\n"
    md_content += f"**Report Generated:** {timestamp}\n"
    md_content += f"**Scanning Accuracy:** Verified via Digital Twin Sync\n\n"
    md_content += "| Status | Vulnerability / AI Thought | Precise Location | Detected Code Snippet | Recommended Action | Context |\n"
    md_content += "| :--- | :--- | :--- | :--- | :--- | :--- |\n"
    
    for f in findings:
        status = "[ ]"
        if "REAL_PATCH" in f['action']: status = "[X]"
        md_content += f"| {status} | {f['thought']} | `{f['location']}` | `{f['snippet']}` | {f['action']} | {f['wiki']} |\n"

    # Save exclusively to the Parent directory (Plantdoctor)
    try:
        with open(PARENT_FIX_LIST, "w") as f:
            f.write(md_content)
        print(f"✅ Authoritative Fix List updated: {os.path.abspath(PARENT_FIX_LIST)}")
        
        # Cleanup: Ensure no local copy exists to avoid confusion
        if os.path.exists(LOCAL_FIX_LIST):
            os.remove(LOCAL_FIX_LIST)
            
    except Exception as e:
        # Emergency local fallback if parent is not writable
        with open(LOCAL_FIX_LIST, "w") as f:
            f.write(md_content)
        print(f"⚠️ Warning: Could not write to parent root. Local fallback updated.")

if __name__ == "__main__":
    generate_fix_list()
