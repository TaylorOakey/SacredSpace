import ollama, json
from pathlib import Path

BASE_DIR = Path("D:/SacredSpace_OS")

# ALIGNED TO YOUR ACTUAL OLLAMA LIST
MODEL_MAP = {
    "elias": "deepseek-r1:1.5b",         
    "claude": "deepseek-r1:1.5b",        
    "aurora": "deepseek-coder:latest",    
    "chatgpt": "deepseek-coder:latest",   
    "default": "phi3:mini"               
}

class CouncilAgent:
    def __init__(self, seat_name):
        self.seat = seat_name.lower()
        self.model = MODEL_MAP.get(self.seat, MODEL_MAP["default"])
        self.soul_path = BASE_DIR / "core" / "souls" / f"{self.seat}.md"
        # We define the client host EXPLICITLY here
        self.client = ollama.Client(host='http://127.0.0.1:11434')

    def speak(self, signal):
        personality = open(self.soul_path, "r").read() if self.soul_path.exists() else "SacredSpace Council Member."
        prompt = f"IDENTITY: {personality}\nSIGNAL: {signal}\nRESPONSE (Max 2 sentences):"
        try:
            # Using the explicit client we just created
            response = self.client.generate(model=self.model, prompt=prompt)
            return response['response']
        except Exception as e:
            return f"∆ [ERROR] Engine failure on {self.model}. Error: {str(e)}"

def get_response(seat, signal):
    return CouncilAgent(seat).speak(signal)
