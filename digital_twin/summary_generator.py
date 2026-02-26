import json
import os
from datetime import datetime

HITS_LOG = "logs/hits.log"
CONSULTANT_LOG = "logs/consultant.log"
SUMMARY_FILE = "logs/summary.log"

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
                hit = json.loads(line)
                if hit["intent"] == "MALICIOUS":
                    malicious_count += 1
                elif hit["intent"] == "BOT":
                    bot_count += 1

    ai_insights_count = 0
    if os.path.exists(CONSULTANT_LOG):
        with open(CONSULTANT_LOG, "r") as f:
            ai_insights_count = f.read().count("[AI] Thought:")

    summary = f"""
--- AegisShield Security Summary ({timestamp}) ---
Traffic Overview:
- Total Hits: {total_hits}
- Malicious Probes: {malicious_count}
- Bot Traffic: {bot_count}

AI Defender Insights:
- Predictions/Actions Taken: {ai_insights_count}

Status: AegisShield is actively protecting the root.
---------------------------------------------------
"""
    with open(SUMMARY_FILE, "a") as f:
        f.write(summary)
    
    return summary

if __name__ == "__main__":
    print(generate_summary())
