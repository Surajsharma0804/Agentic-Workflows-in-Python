"""Plugin management endpoints."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter()

class PluginResponse(BaseModel):
    name: str
    version: str
    description: Optional[str]
    enabled: bool

@router.get("/", response_model=List[PluginResponse])
async def list_plugins():
    """List all available plugins."""
    return [
        PluginResponse(name="file_organizer", version="1.0.0", description="Organize files", enabled=True),
        PluginResponse(name="email_summarizer", version="1.0.0", description="Summarize emails", enabled=True),
        PluginResponse(name="http_task", version="1.0.0", description="HTTP requests", enabled=True),
    ]

@router.get("/{plugin_name}", response_model=PluginResponse)
async def get_plugin(plugin_name: str):
    """Get plugin details."""
    raise HTTPException(status_code=404, detail="Plugin not found")
