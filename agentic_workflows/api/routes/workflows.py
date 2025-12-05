"""Workflow management endpoints."""
from fastapi import APIRouter, HTTPException, status, Depends, Request, BackgroundTasks
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import yaml
import structlog

from ...db.database import get_db
from ...db.models import Workflow, WorkflowExecution, User, AuditLog
from ...core.orchestrator import Orchestrator
from .auth import get_current_user_from_token

logger = structlog.get_logger()
router = APIRouter()


class WorkflowCreate(BaseModel):
    name: str
    description: Optional[str] = None
    spec: str  # YAML string


class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    spec: Optional[str] = None
    is_active: Optional[bool] = None


class WorkflowResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    spec: dict
    is_active: bool
    created_at: str
    updated_at: str


class ExecutionResponse(BaseModel):
    id: str
    workflow_id: str
    status: str
    result: Optional[dict]
    error: Optional[str]
    started_at: Optional[str]
    completed_at: Optional[str]
    created_at: str


def log_audit(db: Session, user_id: int, action: str, resource_type: str, resource_id: str, details: dict, request: Request):
    """Log audit entry."""
    try:
        audit = AuditLog(
            user_id=user_id,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details,
            ip_address=request.client.host if request.client else None,
            user_agent=request.headers.get("user-agent")
        )
        db.add(audit)
        db.commit()
    except Exception as e:
        logger.error("audit_log_failed", error=str(e))


@router.get("/", response_model=List[WorkflowResponse])
async def list_workflows(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """List all workflows for current user."""
    workflows = db.query(Workflow).filter(Workflow.user_id == current_user.id).all()
    return [workflow.to_dict() for workflow in workflows]


@router.post("/", response_model=WorkflowResponse, status_code=status.HTTP_201_CREATED)
async def create_workflow(
    workflow: WorkflowCreate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """Create a new workflow."""
    try:
        # Parse YAML spec
        spec_dict = yaml.safe_load(workflow.spec)
        
        # Create workflow
        db_workflow = Workflow(
            user_id=current_user.id,
            name=workflow.name,
            description=workflow.description,
            spec=spec_dict
        )
        db.add(db_workflow)
        db.commit()
        db.refresh(db_workflow)
        
        # Log audit
        log_audit(db, current_user.id, "create", "workflow", str(db_workflow.id), 
                 {"name": workflow.name}, request)
        
        logger.info("workflow_created", workflow_id=db_workflow.id, user_id=current_user.id)
        return db_workflow.to_dict()
        
    except yaml.YAMLError as e:
        raise HTTPException(status_code=400, detail=f"Invalid YAML: {str(e)}")
    except Exception as e:
        logger.error("workflow_create_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to create workflow")


@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def get_workflow(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """Get workflow by ID."""
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.user_id == current_user.id
    ).first()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    return workflow.to_dict()


@router.put("/{workflow_id}", response_model=WorkflowResponse)
async def update_workflow(
    workflow_id: int,
    workflow_update: WorkflowUpdate,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """Update workflow."""
    db_workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.user_id == current_user.id
    ).first()
    
    if not db_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    try:
        if workflow_update.name:
            db_workflow.name = workflow_update.name
        if workflow_update.description is not None:
            db_workflow.description = workflow_update.description
        if workflow_update.spec:
            db_workflow.spec = yaml.safe_load(workflow_update.spec)
        if workflow_update.is_active is not None:
            db_workflow.is_active = workflow_update.is_active
        
        db_workflow.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(db_workflow)
        
        # Log audit
        log_audit(db, current_user.id, "update", "workflow", str(workflow_id), 
                 {"changes": workflow_update.dict(exclude_none=True)}, request)
        
        logger.info("workflow_updated", workflow_id=workflow_id)
        return db_workflow.to_dict()
        
    except yaml.YAMLError as e:
        raise HTTPException(status_code=400, detail=f"Invalid YAML: {str(e)}")
    except Exception as e:
        logger.error("workflow_update_failed", error=str(e))
        raise HTTPException(status_code=500, detail="Failed to update workflow")


@router.delete("/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_workflow(
    workflow_id: int,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """Delete workflow."""
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.user_id == current_user.id
    ).first()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Log audit before deletion
    log_audit(db, current_user.id, "delete", "workflow", str(workflow_id), 
             {"name": workflow.name}, request)
    
    db.delete(workflow)
    db.commit()
    
    logger.info("workflow_deleted", workflow_id=workflow_id)
    return None


async def run_workflow_background(execution_id: int, workflow_spec: dict, db_session):
    """Run workflow in background."""
    from ...db.database import SessionLocal
    import tempfile
    import os
    
    db = SessionLocal()
    
    try:
        execution = db.query(WorkflowExecution).filter(WorkflowExecution.id == execution_id).first()
        if not execution:
            return
        
        execution.status = "running"
        execution.started_at = datetime.utcnow()
        db.commit()
        
        # Execute workflow using Orchestrator
        # Create temporary file for workflow spec
        with tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False) as f:
            f.write(workflow_spec)
            spec_file = f.name
        
        try:
            orchestrator = Orchestrator()
            result = orchestrator.run_spec(spec_file, dry_run=False)
            
            execution.status = "completed"
            execution.result = {"output": str(result), "status": "success"}
            execution.completed_at = datetime.utcnow()
            db.commit()
            
            logger.info("workflow_execution_completed", execution_id=execution_id)
        finally:
            # Clean up temp file
            if os.path.exists(spec_file):
                os.unlink(spec_file)
        
    except Exception as e:
        execution.status = "failed"
        execution.error = str(e)
        execution.completed_at = datetime.utcnow()
        db.commit()
        logger.error("workflow_execution_failed", execution_id=execution_id, error=str(e))
    finally:
        db.close()


@router.post("/{workflow_id}/execute", response_model=ExecutionResponse)
async def execute_workflow(
    workflow_id: int,
    background_tasks: BackgroundTasks,
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """Execute workflow."""
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.user_id == current_user.id
    ).first()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    if not workflow.is_active:
        raise HTTPException(status_code=400, detail="Workflow is not active")
    
    # Create execution record
    execution = WorkflowExecution(
        workflow_id=workflow_id,
        user_id=current_user.id,
        status="pending"
    )
    db.add(execution)
    db.commit()
    db.refresh(execution)
    
    # Log audit
    log_audit(db, current_user.id, "execute", "workflow", str(workflow_id), 
             {"execution_id": str(execution.id)}, request)
    
    # Run workflow in background
    background_tasks.add_task(run_workflow_background, execution.id, workflow.spec, db)
    
    logger.info("workflow_execution_started", workflow_id=workflow_id, execution_id=execution.id)
    return execution.to_dict()


@router.get("/{workflow_id}/executions", response_model=List[ExecutionResponse])
async def list_executions(
    workflow_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """List all executions for a workflow."""
    workflow = db.query(Workflow).filter(
        Workflow.id == workflow_id,
        Workflow.user_id == current_user.id
    ).first()
    
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    executions = db.query(WorkflowExecution).filter(
        WorkflowExecution.workflow_id == workflow_id
    ).order_by(WorkflowExecution.created_at.desc()).limit(50).all()
    
    return [execution.to_dict() for execution in executions]


@router.get("/executions/{execution_id}", response_model=ExecutionResponse)
async def get_execution(
    execution_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """Get execution by ID."""
    execution = db.query(WorkflowExecution).filter(
        WorkflowExecution.id == execution_id,
        WorkflowExecution.user_id == current_user.id
    ).first()
    
    if not execution:
        raise HTTPException(status_code=404, detail="Execution not found")
    
    return execution.to_dict()
