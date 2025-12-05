"""Audit log endpoints."""
from fastapi import APIRouter, Depends, Request, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import structlog

from ...db.database import get_db
from ...db.models import AuditLog, User
from .auth import get_current_user_from_token

logger = structlog.get_logger()
router = APIRouter()


class AuditLogResponse(BaseModel):
    id: str
    user_id: Optional[str]
    action: str
    resource_type: str
    resource_id: Optional[str]
    details: Optional[dict]
    ip_address: Optional[str]
    user_agent: Optional[str]
    created_at: str


@router.get("/", response_model=List[AuditLogResponse])
async def list_audit_logs(
    resource_type: Optional[str] = Query(None),
    action: Optional[str] = Query(None),
    limit: int = Query(100, le=1000),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """List audit logs for current user."""
    query = db.query(AuditLog).filter(AuditLog.user_id == current_user.id)
    
    if resource_type:
        query = query.filter(AuditLog.resource_type == resource_type)
    if action:
        query = query.filter(AuditLog.action == action)
    
    logs = query.order_by(AuditLog.created_at.desc()).limit(limit).all()
    return [log.to_dict() for log in logs]


@router.get("/{log_id}", response_model=AuditLogResponse)
async def get_audit_log(
    log_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user_from_token)
):
    """Get specific audit log entry."""
    log = db.query(AuditLog).filter(
        AuditLog.id == log_id,
        AuditLog.user_id == current_user.id
    ).first()
    
    if not log:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Audit log not found")
    
    return log.to_dict()
