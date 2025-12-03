"""Task management endpoints."""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

router = APIRouter()

class TaskResponse(BaseModel):
    id: str
    workflow_id: str
    status: str
    created_at: datetime

@router.get("/", response_model=List[TaskResponse])
async def list_tasks():
    """List all tasks."""
    return []

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(task_id: str):
    """Get task by ID."""
    raise HTTPException(status_code=404, detail="Task not found")
