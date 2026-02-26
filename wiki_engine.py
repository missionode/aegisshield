import os
import sys

WIKI_DIR = "wiki"

def search_wiki(term):
    """Searches the wiki/ folder for files containing the search term."""
    results = []
    if not os.path.exists(WIKI_DIR):
        return results

    # Multi-term OR search
    terms = term.lower().split()
    
    for item in os.listdir(WIKI_DIR):
        if item.endswith(".md"):
            file_path = os.path.join(WIKI_DIR, item)
            with open(file_path, "r") as f:
                content = f.read().lower()
                filename = item.lower()
                
                # Match if any term is in filename or content
                if any(t in content or t in filename for t in terms):
                    title = item.replace(".md", "").replace("_", " ")
                    results.append({"title": title, "path": file_path, "snippet": content[:200] + "..."})
    
    return results

def get_wiki_content(file_path):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return f.read()
    return "Not found."

if __name__ == "__main__":
    if len(sys.argv) > 2 and sys.argv[1] == "search":
        term = " ".join(sys.argv[2:])
        matches = search_wiki(term)
        if matches:
            for m in matches:
                print(f"--- {m['title']} ---")
                print(m['snippet'])
                print("-" * 20)
        else:
            print("No matching wiki articles found.")
