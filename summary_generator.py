import json
import os
from datetime import datetime

HITS_LOG = "logs/hits.log"
CONSULTANT_LOG = "logs/consultant.log"
SUMMARY_FILE = "logs/summary.log"
SNAPSHOT_FILE = "logs/startup_snapshot.json"
DECEPTION_PLAN = "logs/deception_plan.json"

def generate_summary():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    total_hits = 0
    malicious_count = 0
    bot_count = 0
    
    if os.path.exists(HITS_LOG):
        with open(HITS_LOG, "r") as f:
            lines = f.readlines()
            total_hits = len(lines)
            for line in lines:
                try:
                    hit = json.loads(line)
                    if "MALICIOUS" in hit["intent"] or "CRITICAL" in hit["intent"]:
                        malicious_count += 1
                    elif hit["intent"] == "BOT":
                        bot_count += 1
                except: pass

    ai_insights_count = 0
    if os.path.exists(CONSULTANT_LOG):
        with open(CONSULTANT_LOG, "r") as f:
            ai_insights_count = f.read().count("[AI] Thought:")

    # Load Deception Info
    deceptive_id = "Standard"
    if os.path.exists(DECEPTION_PLAN):
        with open(DECEPTION_PLAN, "r") as f:
            deceptive_id = json.load(f).get("deceptive_server", "Standard")

    summary_text = f"""
--- AegisShield Security Summary ({timestamp}) ---
Identity: {deceptive_id}
Traffic Overview:
- Total Hits: {total_hits}
- Malicious/Trapped: {malicious_count}
- Bot Traffic: {bot_count}

AI Defender Insights:
- Predictions/Actions: {ai_insights_count}

Status: AegisShield is actively protecting the root.
---------------------------------------------------
"""
    with open(SUMMARY_FILE, "a") as f:
        f.write(summary_text)
    
    # Save Snapshot for Quick Retention
    snapshot = {
        "timestamp": timestamp,
        "total_hits": total_hits,
        "malicious": malicious_count,
        "bots": bot_count,
        "ai_insights": ai_insights_count,
        "deceptive_id": deceptive_id
    }
    with open(SNAPSHOT_FILE, "w") as f:
        json.dump(snapshot, f)
    
    return summary_text

if __name__ == "__main__":
    generate_summary()
