from datetime import datetime
def get_session_greeting():
    hour = datetime.now().hour
    protocol = "Dawn" if 5 <= hour < 12 else "Zenith" if 12 <= hour < 18 else "Dusk"
    return {
        "ritual": f"∆ {protocol} Protocol active.",
        "status": "Nine Pillars Standing.",
        "engine": "DeepSeek/Qwen Local Mesh"
    }
