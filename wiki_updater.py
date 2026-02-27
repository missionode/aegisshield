import urllib.request
import xml.etree.ElementTree as ET
import os
import time
from datetime import datetime

WIKI_DIR = "wiki"
STORY_LOG = "logs/story.log"

def log_story(message):
    timestamp = datetime.now().strftime("%H:%M:%S")
    try:
        with open(STORY_LOG, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
    except:
        pass

def fetch_latest_threat():
    """Fetches the latest cybersecurity advisories from a trusted source (CISA)."""
    # CISA Cybersecurity Advisories RSS Feed
    url = "https://www.cisa.gov/cybersecurity-advisories/all.xml"
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (AegisShield Security Daemon)'})
        with urllib.request.urlopen(req, timeout=10) as response:
            xml_data = response.read()
        root = ET.fromstring(xml_data)
        
        # Parse the first RSS item
        for item in root.findall('.//item'):
            title = item.find('title').text
            description = item.find('description').text
            return title, description
            
    except Exception as e:
        # Fallback if offline or blocked
        return "Automated Framework Vulnerability", "A critical vulnerability was discovered in common web frameworks allowing RCE. Update dependencies immediately."
    
    return "Generic Threat", "Update systems regularly."

def update_wiki():
    log_story("🌐 AI is fetching latest intelligence from Trusted Security Feeds...")
    title, desc = fetch_latest_threat()
    
    log_story(f"🧠 AI analyzing new threat: {title[:50]}...")
    
    # Try to use SLM to format the wiki article
    formatted_content = ""
    try:
        from slm_inference import AegisSLM
        slm = AegisSLM()
        prompt = f"""### System: You are AegisShield, an intellectual and highly efficient Ethical Hacker. 
You are analyzing a new threat to update the local security knowledge base.
Format the following threat into a Wiki Markdown article with three sections: '🛡️ Threat Overview', '🛠️ Prevention', and '🎯 Ethical Pen-Testing Strategy' (suggesting safe, ethical methods to test if our local system is vulnerable).
### User: Threat: {title}. Details: {desc}
### Assistant:"""
        # We access the pipeline directly for a custom prompt format
        outputs = slm.pipe(prompt, max_new_tokens=250, do_sample=True, temperature=0.5)
        formatted_content = outputs[0]["generated_text"].split("### Assistant:")[1].strip()
    except Exception as e:
        # Fallback if SLM fails to load
        formatted_content = f"# {title}\n\n### 🛡️ Threat Overview\n{desc}\n\n### 🛠️ Prevention\n- Monitor system logs.\n- Apply latest patches.\n\n### 🎯 Ethical Pen-Testing Strategy\n- Run authenticated vulnerability scans.\n- Conduct secure code review."

    # Generate a safe filename
    filename = "".join([c for c in title if c.isalpha() or c.isdigit() or c==' ']).rstrip()
    filename = filename.replace(" ", "_")[:40] + "_Advisory.md"
    file_path = os.path.join(WIKI_DIR, filename)
    
    # Save the new knowledge base entry
    if not os.path.exists(WIKI_DIR):
        os.makedirs(WIKI_DIR)
        
    with open(file_path, "w") as f:
        f.write(formatted_content)
        
    log_story(f"📚 AI successfully created new Wiki Knowledge: {filename}")
    
    # PHASE 20: Predictive Correlation
    try:
        import threat_correlator
        threat_correlator.correlate_threat(title, desc)
    except Exception as e:
        pass
        
    print(f"Wiki successfully updated: {filename}")

if __name__ == "__main__":
    update_wiki()
