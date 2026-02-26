import os
import json
import sys

DATASET_DIR = "dataset"
HITS_LOG = "logs/hits.log"

def export_for_training():
    """Converts the hits log into a JSONL dataset for potential fine-tuning."""
    if not os.path.exists(HITS_LOG):
        print("No hits log found to export.")
        return
    
    if not os.path.exists(DATASET_DIR):
        os.makedirs(DATASET_DIR)
        
    output_file = os.path.join(DATASET_DIR, "security_dataset.jsonl")
    
    count = 0
    with open(HITS_LOG, "r") as fin, open(output_file, "w") as fout:
        for line in fin:
            try:
                hit = json.loads(line)
                # Formulate for instruction-based fine-tuning
                entry = {
                    "instruction": f"Analyze the traffic hit and determine the security intent.",
                    "input": f"IP: {hit['ip']}, Method: {hit['method']}, Path: {hit['path']}, UserAgent: {hit['user_agent']}",
                    "output": hit["intent"]
                }
                fout.write(json.dumps(entry) + "
")
                count += 1
            except:
                pass
                
    print(f"Exported {count} hits to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "export":
        export_for_training()
    else:
        print("Usage: python3 ml_lab.py export")
