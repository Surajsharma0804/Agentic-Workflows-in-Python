"""Plugin management endpoints."""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import structlog
import inspect

from ...plugins import FileOrganizer, EmailSummarizer, HTTPTask
from ...plugins.base import PluginBase

router = APIRouter()
logger = structlog.get_logger()

# Plugin registry
PLUGIN_REGISTRY = {
    "file_organizer": {
        "class": FileOrganizer,
        "name": "File Organizer",
        "description": "Organize files by type, date, or custom rules",
        "version": "1.0.0",
        "category": "File Management",
        "parameters": {
            "source_dir": {"type": "string", "required": True, "description": "Source directory path"},
            "target_dir": {"type": "string", "required": False, "description": "Target directory path"},
            "organize_by": {"type": "string", "required": False, "default": "type", "options": ["type", "date", "size"]},
        }
    },
    "email_summarizer": {
        "class": EmailSummarizer,
        "name": "Email Summarizer",
        "description": "Summarize emails using AI",
        "version": "1.0.0",
        "category": "Communication",
        "parameters": {
            "email_content": {"type": "string", "required": True, "description": "Email content to summarize"},
            "max_length": {"type": "integer", "required": False, "default": 200, "description": "Maximum summary length"},
        }
    },
    "http_task": {
        "class": HTTPTask,
        "name": "HTTP Request",
        "description": "Make HTTP requests to external APIs",
        "version": "1.0.0",
        "category": "Integration",
        "parameters": {
            "url": {"type": "string", "required": True, "description": "Request URL"},
            "method": {"type": "string", "required": False, "default": "GET", "options": ["GET", "POST", "PUT", "DELETE", "PATCH"]},
            "headers": {"type": "object", "required": False, "description": "Request headers"},
            "body": {"type": "object", "required": False, "description": "Request body"},
        }
    }
}


class PluginResponse(BaseModel):
    id: str
    name: str
    version: str
    description: str
    category: str
    enabled: bool
    parameters: Dict[str, Any]


class PluginTestRequest(BaseModel):
    parameters: Dict[str, Any]


class PluginTestResponse(BaseModel):
    status: str
    plan: Optional[List[Dict[str, Any]]] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


@router.get("/", response_model=List[PluginResponse])
async def list_plugins():
    """List all available plugins with their metadata."""
    try:
        plugins = []
        for plugin_id, plugin_info in PLUGIN_REGISTRY.items():
            plugins.append(PluginResponse(
                id=plugin_id,
                name=plugin_info["name"],
                version=plugin_info["version"],
                description=plugin_info["description"],
                category=plugin_info["category"],
                enabled=True,
                parameters=plugin_info["parameters"]
            ))
        
        logger.info("plugins_listed", count=len(plugins))
        return plugins
    
    except Exception as e:
        logger.error("list_plugins_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list plugins: {str(e)}"
        )


@router.get("/{plugin_name}", response_model=PluginResponse)
async def get_plugin(plugin_name: str):
    """Get detailed information about a specific plugin."""
    try:
        if plugin_name not in PLUGIN_REGISTRY:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plugin '{plugin_name}' not found"
            )
        
        plugin_info = PLUGIN_REGISTRY[plugin_name]
        
        return PluginResponse(
            id=plugin_name,
            name=plugin_info["name"],
            version=plugin_info["version"],
            description=plugin_info["description"],
            category=plugin_info["category"],
            enabled=True,
            parameters=plugin_info["parameters"]
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("get_plugin_failed", plugin=plugin_name, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get plugin: {str(e)}"
        )


@router.post("/{plugin_name}/test", response_model=PluginTestResponse)
async def test_plugin(plugin_name: str, request: PluginTestRequest):
    """
    Test a plugin with given parameters.
    
    Returns the execution plan without actually executing it.
    """
    try:
        if plugin_name not in PLUGIN_REGISTRY:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plugin '{plugin_name}' not found"
            )
        
        plugin_info = PLUGIN_REGISTRY[plugin_name]
        plugin_class = plugin_info["class"]
        
        # Validate required parameters
        required_params = [
            param_name for param_name, param_info in plugin_info["parameters"].items()
            if param_info.get("required", False)
        ]
        
        missing_params = [p for p in required_params if p not in request.parameters]
        if missing_params:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required parameters: {', '.join(missing_params)}"
            )
        
        # Create plugin instance
        plugin = plugin_class(params=request.parameters)
        
        # Get execution plan
        plan = plugin.plan()
        
        logger.info("plugin_tested", plugin=plugin_name, plan_steps=len(plan))
        
        return PluginTestResponse(
            status="success",
            plan=plan,
            result={"message": "Plugin test successful", "steps": len(plan)}
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("test_plugin_failed", plugin=plugin_name, error=str(e))
        return PluginTestResponse(
            status="error",
            error=str(e)
        )


@router.post("/{plugin_name}/execute", response_model=PluginTestResponse)
async def execute_plugin(plugin_name: str, request: PluginTestRequest):
    """
    Execute a plugin with given parameters.
    
    WARNING: This will actually perform the plugin actions.
    """
    try:
        if plugin_name not in PLUGIN_REGISTRY:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Plugin '{plugin_name}' not found"
            )
        
        plugin_info = PLUGIN_REGISTRY[plugin_name]
        plugin_class = plugin_info["class"]
        
        # Validate required parameters
        required_params = [
            param_name for param_name, param_info in plugin_info["parameters"].items()
            if param_info.get("required", False)
        ]
        
        missing_params = [p for p in required_params if p not in request.parameters]
        if missing_params:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Missing required parameters: {', '.join(missing_params)}"
            )
        
        # Create plugin instance
        plugin = plugin_class(params=request.parameters)
        
        # Execute plugin
        result = plugin.execute()
        
        logger.info("plugin_executed", plugin=plugin_name, status=result.get("status"))
        
        return PluginTestResponse(
            status="success",
            result=result
        )
    
    except HTTPException:
        raise
    except Exception as e:
        logger.error("execute_plugin_failed", plugin=plugin_name, error=str(e))
        return PluginTestResponse(
            status="error",
            error=str(e)
        )
