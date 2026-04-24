from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import uvicorn, sys, json
from pathlib import Path
from datetime import datetime

# Path Discovery
ROOT = Path("D:/SacredSpace_OS")
sys.path.append(str(ROOT))

# Import Local Logic
from council.protocol_router import route as council_route
from systems.agents.council_agents import get_response

app = FastAPI(title="SacredSpace OS Zenith Gateway")

@app.get("/")
async def serve_terminal():
    return FileResponse(ROOT / "systems/fastapi/static/index.html")

class SignalRequest(BaseModel):
    text: str

@app.post("/signal")
def process_signal(request: SignalRequest):
    try:
        routing = council_route(request.text)
        seat = routing.get('seat', 'CHATGPT')
        response = get_response(seat, request.text)
        
        return {
            "seat": seat.upper(),
            "pillar": routing.get('pillar', 'CORE').upper(),
            "response": response
        }
    except Exception as e:
        print(f"KERNEL ERROR: {e}")
        raise HTTPException(status_code=500, detail="Neural feedback loop failure.")

if __name__ == "__main__":
    print("\n⟁ ZENITH TERMINAL IGNITED. THE VEIL IS OPEN. ⟁")
    uvicorn.run(app, host="0.0.0.0", port=8000)
