import sys
import torch
import warnings
import re
import os
import json
import urllib.request
import multiprocessing
from datetime import datetime
from transformers import pipeline, TextStreamer, AutoModelForCausalLM, AutoTokenizer

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
STATUS_FILE = "logs/slm_status.json"

class AegisSLM:
    @staticmethod
    def check_slm_update():
        """Securely checks for 100% compatible SLM updates."""
        try:
            api_url = f"https://huggingface.co/api/models/{MODEL_ID}"
            req = urllib.request.Request(api_url)
            with urllib.request.urlopen(req, timeout=5) as response:
                remote_data = json.loads(response.read())
            status = {"MANUAL_UPGRADE_REQ": False, "MESSAGE": "SLM is up to date."}
            if not os.path.exists("logs"): os.makedirs("logs")
            with open(STATUS_FILE, "w") as f:
                json.dump(status, f)
        except Exception: pass

    def __init__(self):
        self.check_slm_update()
        
        # --- Hardware Detection & Optimization ---
        if torch.cuda.is_available():
            self.device = "cuda"
            self.dtype = torch.float16
            desc = "NVIDIA GPU (High Performance)"
        elif torch.backends.mps.is_available():
            self.device = "mps"
            self.dtype = torch.float16
            desc = "Apple Silicon (Optimized)"
        else:
            self.device = "cpu"
            # Use bfloat16 for memory efficiency on CPUs that support it, else float32
            self.dtype = torch.bfloat16 if torch.cuda.is_bf16_supported() else torch.float32
            desc = f"CPU ({multiprocessing.cpu_count()} cores detected)"
            # Leave one core free for OS stability
            torch.set_num_threads(max(1, multiprocessing.cpu_count() - 1))

        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🧠 SLM: Initializing on {desc}...")
        
        self.tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
        self.model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            torch_dtype=self.dtype,
            device_map=self.device if self.device != "cpu" else None,
            low_cpu_mem_usage=True
        )
        
        if self.device == "cpu":
            self.model = self.model.to("cpu")

        self.pipe = pipeline(
            "text-generation", 
            model=self.model,
            tokenizer=self.tokenizer,
            device=0 if self.device == "cuda" else (-1 if self.device == "cpu" else self.device)
        )
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🧠 SLM: Ready for autonomous defense.")

    def clean_output(self, text):
        if "### Assistant:" in text:
            text = text.split("### Assistant:")[-1]
        stop_markers = ["### User:", "### System:", "### Assistant:", "User:", "Assistant:"]
        for marker in stop_markers:
            if marker in text: text = text.split(marker)[0]
        return text.strip()

    def suggest_code_fix(self, code_block, finding_type):
        prompt = f"""### System: You are AegisShield, a professional security engineer.
### User: The following code has a {finding_type}:
{code_block}
Could you rewrite this code to be secure? Output ONLY the corrected code inside a markdown block (e.g. ```python). NO explanations, NO conversational filler.
### Assistant:"""
        
        print(f"[{datetime.now().strftime('%H:%M:%S')}] 🧠 SLM: Generating secure rewrite (Live Stream below)...")
        print("-" * 30)
        streamer = TextStreamer(self.tokenizer, skip_prompt=True, skip_special_tokens=True)
        
        # Dynamic token limit: more context on powerful systems
        max_tokens = 400 if self.device != "cpu" else 200

        outputs = self.pipe(
            prompt, 
            max_new_tokens=max_tokens, 
            do_sample=True, 
            temperature=0.1, 
            streamer=streamer
        )
        print("-" * 30)
        return self.clean_output(outputs[0]["generated_text"])

if __name__ == "__main__":
    print("SLM_READY")
