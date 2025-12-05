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


class ChatRequest(BaseModel):
    """Request for AI chat."""
    message: str
    context: Optional[Dict[str, Any]] = None
    provider: Optional[str] = None


class GenerateWorkflowRequest(BaseModel):
    """Request to generate workflow from description."""
    description: str
    provider: Optional[str] = None


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


@router.post("/chat")
async def chat_with_ai(request: ChatRequest):
    """
    Chat with AI assistant about workflows and automation.
    
    Provides intelligent responses about workflow design, troubleshooting, and best practices.
    """
    try:
        llm = get_llm_provider(request.provider)
        
        if not llm.is_available():
            return {
                "status": "unavailable",
                "message": "AI provider not available. Using fallback response.",
                "response": "I'm currently running in demo mode. To enable full AI capabilities, please configure an LLM provider (OpenAI or Claude) in your environment variables."
            }
        
        # Build context-aware prompt
        system_prompt = """You are an AI assistant for Agentic Workflows, an enterprise workflow automation platform.
You help users design, troubleshoot, and optimize their workflows. Be concise, practical, and focus on actionable advice."""
        
        context_info = ""
        if request.context:
            context_info = f"\n\nContext: {request.context}"
        
        full_prompt = f"{system_prompt}\n\nUser: {request.message}{context_info}\n\nAssistant:"
        
        response = await llm.complete(full_prompt)
        
        return {
            "status": "success",
            "response": response.content,
            "provider": response.model,
            "tokens_used": response.tokens_used
        }
    
    except Exception as e:
        logger.error("chat_failed", error=str(e))
        # Provide fallback response
        return {
            "status": "fallback",
            "response": "I'm here to help with workflow automation! I can assist with:\n\n• Designing workflows\n• Troubleshooting errors\n• Optimizing performance\n• Best practices\n\nWhat would you like to know?",
            "note": "AI provider unavailable, showing fallback response"
        }


@router.post("/generate-workflow")
async def generate_workflow(request: GenerateWorkflowRequest):
    """
    Generate a workflow specification from natural language description.
    
    Uses AI to convert user requirements into a structured workflow YAML.
    """
    try:
        llm = get_llm_provider(request.provider)
        
        if not llm.is_available():
            # Return a template workflow
            template = {
                "name": "Generated Workflow",
                "description": request.description,
                "tasks": [
                    {
                        "id": "task_1",
                        "type": "http_task",
                        "params": {
                            "url": "https://api.example.com/data",
                            "method": "GET"
                        }
                    }
                ],
                "note": "This is a template. Configure an AI provider for intelligent workflow generation."
            }
            return {
                "status": "template",
                "workflow": template,
                "message": "AI provider not available. Returning template workflow."
            }
        
        # Build workflow generation prompt
        prompt = f"""Generate a workflow specification in YAML format for the following requirement:

{request.description}

The workflow should include:
- A descriptive name
- Clear description
- List of tasks with appropriate plugins (file_organizer, email_summarizer, http_task)
- Task dependencies if needed
- Proper error handling

Return only valid YAML that follows this structure:
```yaml
name: Workflow Name
description: Description
tasks:
  - id: task_1
    type: plugin_name
    params:
      key: value
    depends_on: []
```"""
        
        response = await llm.complete(prompt)
        
        # Extract YAML from response
        import yaml
        import re
        
        # Try to extract YAML from code blocks
        yaml_match = re.search(r'```(?:yaml)?\n(.*?)\n```', response.content, re.DOTALL)
        if yaml_match:
            yaml_content = yaml_match.group(1)
        else:
            yaml_content = response.content
        
        try:
            workflow_spec = yaml.safe_load(yaml_content)
        except yaml.YAMLError:
            # If parsing fails, return raw response
            workflow_spec = {
                "name": "Generated Workflow",
                "description": request.description,
                "raw_response": response.content
            }
        
        return {
            "status": "success",
            "workflow": workflow_spec,
            "provider": response.model,
            "tokens_used": response.tokens_used
        }
    
    except Exception as e:
        logger.error("generate_workflow_failed", error=str(e))
        # Return template on error
        template = {
            "name": "Generated Workflow",
            "description": request.description,
            "tasks": [
                {
                    "id": "task_1",
                    "type": "http_task",
                    "params": {
                        "url": "https://api.example.com/data",
                        "method": "GET"
                    }
                }
            ]
        }
        return {
            "status": "error",
            "workflow": template,
            "error": str(e),
            "message": "Failed to generate workflow. Returning template."
        }


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
