import os
import json
import sys
import datetime

NODES_FILE = "logs/nodes.json"
STORY_LOG = "logs/story.log"

def log_story(message):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    try:
        with open(STORY_LOG, "a") as f:
            f.write(f"[{timestamp}] 🛰️ C2: {message}\n")
    except: pass

def initialize_nodes(default_root):
    if not os.path.exists("logs"): os.makedirs("logs")
    
    if not os.path.exists(NODES_FILE):
        # Default to the parent directory as the first node
        initial_nodes = [os.path.abspath(default_root)]
        with open(NODES_FILE, "w") as f:
            json.dump(initial_nodes, f, indent=4)
        log_story(f"C2 Registry initialized with default node: {default_root}")
    else:
        log_story("C2 Registry loaded. Ready to protect multiple nodes.")

def add_nodes(paths):
    if not os.path.exists(NODES_FILE):
        nodes = []
    else:
        with open(NODES_FILE, "r") as f:
            nodes = json.load(f)
            
    added_count = 0
    for path in paths:
        abs_path = os.path.abspath(path)
        if not os.path.exists(abs_path):
            print(f"Error: Path {path} does not exist.")
            continue
        
        if abs_path not in nodes:
            nodes.append(abs_path)
            log_story(f"Added new node to protection registry: {abs_path}")
            print(f"Node added: {abs_path}")
            added_count += 1
        else:
            print(f"Node already registered: {abs_path}")
            
    if added_count > 0:
        with open(NODES_FILE, "w") as f:
            json.dump(nodes, f, indent=4)

def get_nodes():
    if not os.path.exists(NODES_FILE): return []
    with open(NODES_FILE, "r") as f:
        return json.load(f)

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "add":
        add_nodes(sys.argv[2:])
    elif len(sys.argv) > 1 and sys.argv[1] == "init":
        initialize_nodes(sys.argv[2] if len(sys.argv) > 2 else "..")
    elif len(sys.argv) > 1 and sys.argv[1] == "list":
        for n in get_nodes(): print(n)
    else:
        nodes = get_nodes()
        print("Registered AegisShield Nodes:")
        for n in nodes: print(f" - {n}")
