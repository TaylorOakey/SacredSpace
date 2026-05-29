import os, requests
from datetime import datetime
OLLAMA_HOST  = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
GEMINI_KEY   = os.environ.get("GEMINI_API_KEY", "")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.0-flash")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.2")

class OllamaProvider:
    name = "ollama"
    def available(self):
        try:
            r = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=3)
            return any(OLLAMA_MODEL.split(":")[0] in m["name"] for m in r.json().get("models",[]))
        except:
            return False
    def generate(self, prompt, system=""):
        msgs = ([{"role":"system","content":system}] if system else []) + [{"role":"user","content":prompt}]
        r = requests.post(f"{OLLAMA_HOST}/api/chat", json={"model":OLLAMA_MODEL,"stream":False,"messages":msgs}, timeout=120)
        r.raise_for_status()
        d = r.json()
        return {"text":d.get("message",{}).get("content",""),"provider":self.name,"model":OLLAMA_MODEL,"tokens":d.get("eval_count",0)}

class GeminiProvider:
    name = "gemini"
    def available(self):
        return bool(GEMINI_KEY)
    def generate(self, prompt, system=""):
        full = f"{system}\n\n{prompt}" if system else prompt
        r = requests.post(f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GEMINI_KEY}",
            json={"contents":[{"parts":[{"text":full}]}],"generationConfig":{"maxOutputTokens":1024}}, timeout=60)
        r.raise_for_status()
        d = r.json()
        text = d.get("candidates",[{}])[0].get("content",{}).get("parts",[{}])[0].get("text","")
        return {"text":text,"provider":self.name,"model":GEMINI_MODEL,"tokens":d.get("usageMetadata",{}).get("totalTokenCount",0)}

class MockProvider:
    name = "mock"
    def available(self):
        return True
    def generate(self, prompt, system=""):
        return {"text":f"[MockLLM] {prompt[:120]}","provider":self.name,"model":"mock","tokens":0}

class InferenceCascade:
    def __init__(self):
        self.providers = [OllamaProvider(), GeminiProvider(), MockProvider()]
    def generate(self, prompt, system=""):
        errors = []
        for p in self.providers:
            if not p.available():
                errors.append(f"{p.name}: not available")
                continue
            try:
                r = p.generate(prompt, system)
                r.update({"cascade_errors":errors,"timestamp":datetime.utcnow().isoformat()})
                print(f"[CASCADE] Fired: {p.name}")
                return r
            except Exception as e:
                errors.append(f"{p.name}: {e}")
                print(f"[CASCADE] {p.name} failed - {e}")
        return {"text":"[CASCADE FAILURE]","provider":"none","model":"none","tokens":0,"cascade_errors":errors}
    def status(self):
        return {p.name: p.available() for p in self.providers}

cascade = InferenceCascade()
