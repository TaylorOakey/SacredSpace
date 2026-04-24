import os, sys, json
from pathlib import Path
from datetime import datetime

# OS Path Alignment
ROOT = Path("D:/SacredSpace_OS")
sys.path.append(str(ROOT))
from systems.agents.council_agents import get_response

class TheForge:
    def __init__(self):
        self.seed_path = ROOT / "economy" / "studios" / "seeds"
        self.signal_path = ROOT / "economy" / "studios" / "signals"

    def manifest_signal(self, seed_text):
        """Transforms raw lore into social signals."""
        print(f"∆ Distilling Seed: {seed_text[:30]}...")
        
        # We call the Council (Ollama) to format the posts
        x_post = get_response("AURORA", f"Turn this into a high-signal Tweet with tags: {seed_text}")
        ig_caption = get_response("CLAUDE", f"Write a poetic Instagram caption for this: {seed_text}")
        yt_desc = get_response("CHATGPT", f"Create a YouTube description and title for this: {seed_text}")
        
        signal_data = {
            "timestamp": datetime.now().isoformat(),
            "seed": seed_text,
            "deployments": {
                "X": x_post,
                "Instagram": ig_caption,
                "YouTube": yt_desc
            },
            "status": "READY_TO_SHIP"
        }
        
        # Save to a local file for deployment
        filename = f"signal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(self.signal_path / filename, "w") as f:
            json.dump(signal_data, f, indent=4)
        
        return filename

if __name__ == "__main__":
    forge = TheForge()
    # Example: Creating a signal from a core mantra
    file = forge.manifest_signal("The Nine Pillars are standing. The OS is breathing local air.")
    print(f"✓ Signal crystallized in signals/{file} ∆")
