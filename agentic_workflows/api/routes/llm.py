"""LLM-powered AI endpoints."""
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
import structlog

from ...agents import PlannerAgent, RecoveryAgent, ValidatorAgent
from ...core.spec import WorkflowSpec, load_spec
from ...llm import get_llm_provider

router = APIRouter()
logger = structlog.get_logger()


class PlanRequest(BaseModel):
    """Request to plan a workflow."""
    workflow_spec: Dict[str, Any]
    provider: Optional[str] = None


class RecoveryRequest(BaseModel):
    """Request for error recovery suggestions."""
    task_id: str
    error_message: str
    task_context: Dict[str, Any]
    provider: Optional[str] = None


class ValidationRequest(BaseModel):
    """Request to validate a workflow."""
    workflow_spec: Dict[str, Any]
    auto_fix: bool = False
    provider: Optional[str] = None


class LLMTestRequest(BaseModel):
    """Request to test LLM provider."""
    provider: str
    prompt: str


@router.post("/plan")
async def plan_workflow(request: PlanRequest):
    """
    Generate AI-powered execution plan for a workflow.
    
    Uses LLM to analyze the workflow and suggest optimal execution strategy.
    """
    try:
        # Create workflow spec from dict
        spec = WorkflowSpec(**request.workflow_spec)
        
        # Create planner with specified provider
        llm = get_llm_provider(request.provider) if request.provider else None
        planner = PlannerAgent(llm_provider=llm)
        
        # Generate plan
        plan = await planner.plan_workflow(spec)
        
        # Get explanation
        explanation = await planner.explain_plan(plan)
        
        return {
            "status": "success",
            "plan": plan,
            "explanation": explanation,
            "provider": planner.llm.model
        }
    
    except Exception as e:
        logger.error("plan_workflow_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to plan workflow: {str(e)}"
        )


@router.post("/recover")
async def recover_from_error(request: RecoveryRequest):
    """
    Get AI-powered recovery suggestions for a failed task.
    
    Analyzes the error and suggests specific recovery actions.
    """
    try:
        # Create recovery agent
        llm = get_llm_provider(request.provider) if request.provider else None
        recovery = RecoveryAgent(llm_provider=llm)
        
        # Analyze failure
        recovery_plan = await recovery.analyze_failure(
            task_id=request.task_id,
            error_message=request.error_message,
            task_context=request.task_context
        )
        
        return {
            "status": "success",
            "recovery_plan": recovery_plan,
            "provider": recovery.llm.model
        }
    
    except Exception as e:
        logger.error("recovery_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to generate recovery plan: {str(e)}"
        )


@router.post("/validate")
async def validate_workflow(request: ValidationRequest):
    """
    Validate workflow specification using AI.
    
    Checks for errors, warnings, and suggests improvements.
    """
    try:
        # Create workflow spec from dict
        spec = WorkflowSpec(**request.workflow_spec)
        
        # Create validator
        llm = get_llm_provider(request.provider) if request.provider else None
        validator = ValidatorAgent(llm_provider=llm)
        
        # Validate
        is_valid, issues, fixed_spec = await validator.validate_workflow(
            spec,
            auto_fix=request.auto_fix
        )
        
        # Get suggestions if valid
        suggestions = []
        if is_valid:
            suggestions = await validator.suggest_improvements(spec)
        
        return {
            "status": "success",
            "is_valid": is_valid,
            "issues": issues,
            "suggestions": suggestions,
            "fixed_spec": fixed_spec.dict() if fixed_spec else None,
            "provider": validator.llm.model
        }
    
    except Exception as e:
        logger.error("validation_failed", error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to validate workflow: {str(e)}"
        )


@router.post("/test")
async def test_llm_provider(request: LLMTestRequest):
    """
    Test LLM provider connectivity and response.
    
    Useful for verifying API keys and provider availability.
    """
    try:
        llm = get_llm_provider(request.provider)
        
        if not llm.is_available():
            return {
                "status": "unavailable",
                "provider": request.provider,
                "message": "Provider not available (check API key)"
            }
        
        response = await llm.complete(request.prompt)
        
        return {
            "status": "success",
            "provider": request.provider,
            "model": response.model,
            "response": response.content,
            "tokens_used": response.tokens_used
        }
    
    except Exception as e:
        logger.error("llm_test_failed", provider=request.provider, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM test failed: {str(e)}"
        )


@router.get("/providers")
async def list_providers():
    """List available LLM providers and their status."""
    providers = []
    
    for provider_name in ["openai", "claude", "dummy"]:
        try:
            llm = get_llm_provider(provider_name)
            providers.append({
                "name": provider_name,
                "available": llm.is_available(),
                "model": llm.model
            })
        except Exception as e:
            providers.append({
                "name": provider_name,
                "available": False,
                "error": str(e)
            })
    
    return {
        "status": "success",
        "providers": providers
    }
