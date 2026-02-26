import sys
import torch
import warnings
import re
from transformers import pipeline

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

class AegisSLM:
    def __init__(self):
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
        prompt = f"""### System: You are AegisShield, an AI security expert.
### User: I found a {finding_type} vulnerability at {path}. What is your expert assessment? (Be concise)
### Assistant:"""
        outputs = self.pipe(prompt, max_new_tokens=100, do_sample=True, temperature=0.7)
        return self.clean_output(outputs[0]["generated_text"])

    def suggest_code_fix(self, code_block, finding_type):
        prompt = f"""### System: You are AegisShield, a Senior Security Engineer.
### User: The following code has a {finding_type}:
{code_block}
Rewrite this code to be secure while maintaining its functionality. Provide only the secure code block.
### Assistant:"""
        outputs = self.pipe(prompt, max_new_tokens=200, do_sample=True, temperature=0.2)
        return self.clean_output(outputs[0]["generated_text"])

    def review_code_logic(self, code_block, finding_type):
        prompt = f"""### System: You are AegisShield, a Senior Security Engineer.
### User: Review this code block for a potential {finding_type}:
{code_block}
Is this truly dangerous? Provide a concise one-sentence verdict.
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
        prompt = f"""### System: You are AegisShield, a SOC Analyst AI.
### User: Analyze this batch of web traffic hits:
{traffic_batch}
Determine if there is a coordinated attack pattern. Concise summary only.
### Assistant:"""
        outputs = self.pipe(prompt, max_new_tokens=150, do_sample=True, temperature=0.4)
        return self.clean_output(outputs[0]["generated_text"])

if __name__ == "__main__":
    print("SLM_READY")
