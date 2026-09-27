#!/usr/bin/env python3
"""
SacredSpace FIAHFOX Bridge Engine
Manages the SacredSpace Bus for inter-agent communication and event routing.
"""

import os
import sys
import json
import time
import asyncio
import threading
import requests
from datetime import datetime
from typing import Dict, List, Any, Callable, Optional
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import uvicorn
import websockets
import logging

# Configuration
BUS_PORT = int(os.getenv('BUS_PORT', '7777'))
API_URL = os.getenv('API_URL', 'http://127.0.0.1:8000')
OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Logging
logging.basicConfig(level=getattr(logging, LOG_LEVEL))
logger = logging.getLogger(__name__)

class Event(BaseModel):
    event: str
    data: Dict[str, Any]
    source: Optional[str] = None
    timestamp: Optional[str] = None

class Agent:
    """Represents a connected agent."""
    
    def __init__(self, name: str, capabilities: List[str], websocket=None):
        self.name = name
        self.capabilities = capabilities
        self.websocket = websocket
        self.last_seen = datetime.now()
        self.status = 'connected'

class SacredSpaceBus:
    """Central event bus for SacredSpace agents."""
    
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.event_handlers: Dict[str, List[Callable]] = {}
        self.event_history: List[Dict[str, Any]] = []
        self.max_history = 1000
        
    def register_agent(self, name: str, capabilities: List[str], websocket=None) -> bool:
        """Register an agent with the bus."""
        if name in self.agents:
            logger.warning(f"Agent {name} already registered, updating")
        
        self.agents[name] = Agent(name, capabilities, websocket)
        logger.info(f"Registered agent: {name} with capabilities: {capabilities}")
        
        # Emit agent_join event
        self.emit_event('agent_join', {
            'agent': name,
            'capabilities': capabilities,
            'timestamp': datetime.now().isoformat()
        })
        
        return True
    
    def unregister_agent(self, name: str):
        """Unregister an agent."""
        if name in self.agents:
            del self.agents[name]
            logger.info(f"Unregistered agent: {name}")
            
            # Emit agent_leave event
            self.emit_event('agent_leave', {
                'agent': name,
                'timestamp': datetime.now().isoformat()
            })
    
    def emit_event(self, event: str, data: Dict[str, Any], source: str = None):
        """Emit an event to all registered handlers and agents."""
        event_data = {
            'event': event,
            'data': data,
            'source': source or 'bus',
            'timestamp': datetime.now().isoformat()
        }
        
        # Add to history
        self.event_history.append(event_data)
        if len(self.event_history) > self.max_history:
            self.event_history.pop(0)
        
        logger.info(f"Event emitted: {event} from {source}")
        
        # Call local handlers
        if event in self.event_handlers:
            for handler in self.event_handlers[event]:
                try:
                    handler(event_data)
                except Exception as e:
                    logger.error(f"Handler error for {event}: {e}")
        
        # Send to WebSocket agents
        for agent in self.agents.values():
            if agent.websocket:
                try:
                    asyncio.create_task(
                        agent.websocket.send(json.dumps(event_data))
                    )
                except Exception as e:
                    logger.error(f"WebSocket send error to {agent.name}: {e}")
    
    def on_event(self, event: str, handler: Callable):
        """Register an event handler."""
        if event not in self.event_handlers:
            self.event_handlers[event] = []
        self.event_handlers[event].append(handler)
        logger.debug(f"Registered handler for event: {event}")
    
    def get_agents(self) -> Dict[str, Dict[str, Any]]:
        """Get all registered agents."""
        return {
            name: {
                'capabilities': agent.capabilities,
                'status': agent.status,
                'last_seen': agent.last_seen.isoformat()
            }
            for name, agent in self.agents.items()
        }
    
    def get_event_history(self, limit: int = 50) -> List[Dict[str, Any]]:
        """Get recent event history."""
        return self.event_history[-limit:]

# Global bus instance
bus = SacredSpaceBus()

# FastAPI app
app = FastAPI(title="SacredSpace FIAHFOX Bridge", version="1.0.0")

@app.post("/bus/emit")
async def emit_event(event: Event, background_tasks: BackgroundTasks):
    """Emit an event to the bus."""
    try:
        bus.emit_event(event.event, event.data, event.source)
        return {"status": "emitted", "event": event.event}
    except Exception as e:
        logger.error(f"Emit error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/bus/agents")
async def get_agents():
    """Get registered agents."""
    return bus.get_agents()

@app.get("/bus/history")
async def get_history(limit: int = 50):
    """Get event history."""
    return bus.get_event_history(limit)

@app.post("/bus/register")
async def register_agent(name: str, capabilities: List[str]):
    """Register an agent."""
    try:
        bus.register_agent(name, capabilities)
        return {"status": "registered", "agent": name}
    except Exception as e:
        logger.error(f"Register error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "agents": len(bus.agents),
        "events": len(bus.event_history)
    }

# WebSocket handler
async def websocket_handler(websocket, path):
    """Handle WebSocket connections."""
    try:
        # First message should be agent registration
        message = await websocket.recv()
        data = json.loads(message)
        
        if data.get('type') == 'register':
            agent_name = data.get('name')
            capabilities = data.get('capabilities', [])
            
            if agent_name:
                bus.register_agent(agent_name, capabilities, websocket)
                
                # Keep connection alive and handle messages
                async for message in websocket:
                    try:
                        event_data = json.loads(message)
                        if 'event' in event_data:
                            bus.emit_event(
                                event_data['event'], 
                                event_data.get('data', {}), 
                                agent_name
                            )
                    except json.JSONDecodeError:
                        logger.warning(f"Invalid JSON from {agent_name}")
                    except Exception as e:
                        logger.error(f"WebSocket message error from {agent_name}: {e}")
            else:
                await websocket.close()
        else:
            await websocket.close()
            
    except websockets.exceptions.ConnectionClosed:
        logger.info("WebSocket connection closed")
    except Exception as e:
        logger.error(f"WebSocket handler error: {e}")
    finally:
        # Find and unregister agent
        for name, agent in bus.agents.items():
            if agent.websocket == websocket:
                bus.unregister_agent(name)
                break

# Event handlers
def on_memory_sealed(event_data):
    """Handle memory_sealed events."""
    data = event_data['data']
    logger.info(f"Memory sealed: {data.get('vault_path', 'unknown')}")
    
    # Could trigger learning loops, notifications, etc.

def on_agent_query(event_data):
    """Handle agent_query events."""
    data = event_data['data']
    query = data.get('query', '')
    logger.info(f"Agent query: {query}")
    
    # Could route to appropriate agents, trigger searches, etc.

# Register handlers
bus.on_event('memory_sealed', on_memory_sealed)
bus.on_event('agent_query', on_agent_query)

async def start_websocket_server():
    """Start WebSocket server."""
    server = await websockets.serve(
        websocket_handler, 
        "0.0.0.0", 
        BUS_PORT + 1  # WebSocket on BUS_PORT + 1
    )
    logger.info(f"WebSocket server started on port {BUS_PORT + 1}")
    await server.wait_closed()

def run_websocket_server():
    """Run WebSocket server in thread."""
    asyncio.run(start_websocket_server())

def main():
    """Main entry point."""
    logger.info("Starting SacredSpace FIAHFOX Bridge")
    
    # Start WebSocket server in background thread
    ws_thread = threading.Thread(target=run_websocket_server, daemon=True)
    ws_thread.start()
    
    # Start FastAPI server
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=BUS_PORT,
        log_level=LOG_LEVEL.lower()
    )

if __name__ == '__main__':
    main()