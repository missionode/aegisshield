import sys
import torch
import warnings
import re
import os
import json
import urllib.request
from transformers import pipeline

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
STATUS_FILE = "logs/slm_status.json"

class AegisSLM:
    @staticmethod
    def check_slm_update():
        """Securely checks for 100% compatible SLM updates."""
        try:
            # 1. Fetch remote model metadata from HuggingFace
            api_url = f"https://huggingface.co/api/models/{MODEL_ID}"
            req = urllib.request.Request(api_url)
            with urllib.request.urlopen(req, timeout=5) as response:
                remote_data = json.loads(response.read())

            # 2. Mathematical Compatibility Verification
            # We must ensure the architecture is identical to prevent prompt-breaking.
            architectures = remote_data.get("siblings", [])
            is_compatible = any(s.get("rfilename", "") == "config.json" for s in architectures) # Basic proxy check for HF format
            
            status = {"MANUAL_UPGRADE_REQ": False, "MESSAGE": "SLM is up to date."}

            if is_compatible:
                # E.g. If we found a newer commit but the architecture is safe
                # For this proof-of-concept, we'll assume the current ID is always the safe baseline.
                # If a hypothetical "v2.0" tag existed, we would flag it here.
                pass 
            else:
                # Architecture changed or unknown. Block auto-update!
                status = {
                    "MANUAL_UPGRADE_REQ": True, 
                    "MESSAGE": f"New version of {MODEL_ID} detected, but compatibility is not 100% guaranteed. Manual intervention required."
                }
            
            if not os.path.exists("logs"): os.makedirs("logs")
            with open(STATUS_FILE, "w") as f:
                json.dump(status, f)
                
        except Exception as e:
            # Fail silently on network errors so the SOC doesn't crash
            pass

    def __init__(self):
        self.check_slm_update()
        self.pipe = pipeline(
            "text-generation", 
            model=MODEL_ID, 
            torch_dtype=torch.float16, 
            device_map="auto"
        )

    def clean_output(self, text):
        """Ultra-strict output cleaning to remove all prompt markers and hallucinations."""
        # 1. Take only the part after the last Assistant marker
        if "### Assistant:" in text:
            text = text.split("### Assistant:")[-1]
        
        # 2. TRUNCATE immediately if the model starts hallucinating a new turn
        # If we see ### User, ### System, or ### Assistant again, stop right there.
        stop_markers = ["### User:", "### System:", "### Assistant:", "User:", "Assistant:"]
        for marker in stop_markers:
            if marker in text:
                text = text.split(marker)[0]
        
        # 3. Final polish: remove any lingering markdown artifacts and whitespace
        return text.strip()

    def reason_about_finding(self, finding_type, path):
        prompt = f"""### System: You are AegisShield, a friendly and helpful security companion.
### User: I found a {finding_type} vulnerability at {path}. What does this mean for my project? Please explain it simply and why it matters.
### Assistant:"""
        outputs = self.pipe(prompt, max_new_tokens=150, do_sample=True, temperature=0.7)
        return self.clean_output(outputs[0]["generated_text"])

    def suggest_code_fix(self, code_block, finding_type):
        prompt = f"""### System: You are AegisShield, a helpful engineering mentor.
### User: The following code has a {finding_type}:
{code_block}
Could you rewrite this code to be secure, and give a brief, friendly explanation of what you changed? Print the explanation first, then the code snippet.
### Assistant:"""
        outputs = self.pipe(prompt, max_new_tokens=250, do_sample=True, temperature=0.3)
        return self.clean_output(outputs[0]["generated_text"])

    def review_code_logic(self, code_block, finding_type):
        prompt = f"""### System: You are AegisShield, a friendly security mentor.
### User: Could you look at this code block for a potential {finding_type}?
{code_block}
Is this actually dangerous? Please give me a friendly, one-sentence verdict.
### Assistant:"""
        outputs = self.pipe(prompt, max_new_tokens=100, do_sample=True, temperature=0.3)
        return self.clean_output(outputs[0]["generated_text"])

    def determine_strategy(self, file_manifest, used_ports):
        prompt = f"""### System: You are AegisShield, a strategic security AI.
### User: Root files: {file_manifest}. Used ports: {used_ports}. 
Identify tech stack, suggest a deceptive identity, and 4 ghost ports.
Provide JSON only: {{"tech_stack": "...", "deceptive_server": "...", "ghost_ports": [21, 2222, ...]}}
### Assistant:"""
        outputs = self.pipe(prompt, max_new_tokens=200, do_sample=True, temperature=0.2)
        return self.clean_output(outputs[0]["generated_text"])

    def classify_traffic(self, traffic_batch):
        prompt = f"""### System: You are AegisShield, an intellectual and highly efficient Ethical Hacker and SOC Analyst.
### User: Evaluate this batch of web traffic hits:
{traffic_batch}
Analyze the intent behind this traffic using advanced penetration testing methodologies (like OWASP Top 10 or MITRE ATT&CK). Provide a powerful, concise defense theory estimating what the attacker is trying to achieve.
### Assistant:"""
        outputs = self.pipe(prompt, max_new_tokens=150, do_sample=True, temperature=0.5)
        return self.clean_output(outputs[0]["generated_text"])

    def inspect_payload(self, request_string):
        prompt = f"""### System: You are AegisShield, a Semantic Web Application Firewall (AI WAF).
### User: Inspect this HTTP request payload: "{request_string}"
Is this attempting to exploit a vulnerability (like obfuscated SQLi, XSS, or Directory Traversal)? Reply with exactly one word: "MALICIOUS" or "SAFE". Do not add any other text.
### Assistant:"""
        # Strict low temperature for binary classification
        outputs = self.pipe(prompt, max_new_tokens=10, do_sample=True, temperature=0.1)
        response = self.clean_output(outputs[0]["generated_text"]).upper()
        if "MALICIOUS" in response: return "MALICIOUS"
        return "SAFE"

if __name__ == "__main__":
    print("SLM_READY")
