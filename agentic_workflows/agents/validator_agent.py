"""Validator Agent - Validates and auto-fixes workflow specs using LLM."""
from typing import Dict, Any, List, Optional, Tuple
import json
import structlog

from .base_agent import BaseAgent
from ..core.spec import WorkflowSpec

logger = structlog.get_logger()


class ValidatorAgent(BaseAgent):
    """AI-powered workflow validator."""
    
    def get_system_prompt(self) -> str:
        return """You are an expert workflow validation AI assistant. Your role is to:

1. Validate workflow specifications for correctness
2. Identify potential issues and errors
3. Suggest fixes and improvements
4. Ensure best practices are followed
5. Auto-fix common problems when possible

Be thorough, specific, and prioritize safety and reliability."""
    
    def fallback_response(self, prompt: str) -> str:
        return json.dumps({
            "valid": True,
            "issues": [],
            "suggestions": ["Unable to perform AI validation, using basic checks"]
        })
    
    async def validate_workflow(
        self,
        spec: WorkflowSpec,
        auto_fix: bool = False
    ) -> Tuple[bool, List[Dict[str, Any]], Optional[WorkflowSpec]]:
        """
        Validate a workflow specification.
        
        Args:
            spec: Workflow specification to validate
            auto_fix: Whether to attempt automatic fixes
        
        Returns:
            Tuple of (is_valid, issues, fixed_spec)
        """
        self.log_action("validating_workflow", workflow_id=spec.id, auto_fix=auto_fix)
        
        # Basic validation
        basic_issues = self._basic_validation(spec)
        
        # LLM-powered validation
        prompt = self._build_validation_prompt(spec)
        llm_response = await self.think(prompt)
        
        llm_issues = self._parse_validation_response(llm_response)
        
        all_issues = basic_issues + llm_issues
        is_valid = len([i for i in all_issues if i["severity"] == "error"]) == 0
        
        fixed_spec = None
        if auto_fix and not is_valid:
            fixed_spec = await self._auto_fix(spec, all_issues)
        
        self.log_action(
            "validation_complete",
            workflow_id=spec.id,
            is_valid=is_valid,
            issue_count=len(all_issues)
        )
        
        return is_valid, all_issues, fixed_spec
    
    def _basic_validation(self, spec: WorkflowSpec) -> List[Dict[str, Any]]:
        """Perform basic validation checks."""
        issues = []
        
        # Check required fields
        if not spec.id:
            issues.append({
                "severity": "error",
                "field": "id",
                "message": "Workflow ID is required",
                "fix": "Add a unique workflow ID"
            })
        
        if not spec.name:
            issues.append({
                "severity": "error",
                "field": "name",
                "message": "Workflow name is required",
                "fix": "Add a descriptive workflow name"
            })
        
        if not spec.tasks or len(spec.tasks) == 0:
            issues.append({
                "severity": "error",
                "field": "tasks",
                "message": "Workflow must have at least one task",
                "fix": "Add tasks to the workflow"
            })
        
        # Check task IDs are unique
        task_ids = [task.id for task in spec.tasks]
        if len(task_ids) != len(set(task_ids)):
            issues.append({
                "severity": "error",
                "field": "tasks",
                "message": "Task IDs must be unique",
                "fix": "Ensure each task has a unique ID"
            })
        
        # Check each task
        for i, task in enumerate(spec.tasks):
            if not task.id:
                issues.append({
                    "severity": "error",
                    "field": f"tasks[{i}].id",
                    "message": f"Task {i+1} is missing an ID",
                    "fix": f"Add an ID to task {i+1}"
                })
            
            if not task.type:
                issues.append({
                    "severity": "error",
                    "field": f"tasks[{i}].type",
                    "message": f"Task {task.id} is missing a type",
                    "fix": f"Specify a plugin type for task {task.id}"
                })
        
        return issues
    
    def _build_validation_prompt(self, spec: WorkflowSpec) -> str:
        """Build prompt for workflow validation."""
        tasks_desc = "\n".join([
            f"- {task.id}: type={task.type}, params={list(task.params.keys())}"
            for task in spec.tasks
        ])
        
        return f"""Validate this workflow specification and identify any issues:

**Workflow**: {spec.name} (ID: {spec.id})
**Description**: {spec.description}

**Tasks**:
{tasks_desc}

Check for:
1. Logical errors or inconsistencies
2. Missing required parameters
3. Potential runtime issues
4. Security concerns
5. Performance bottlenecks
6. Best practice violations

For each issue, provide:
- Severity (error, warning, info)
- Description
- Suggested fix

Format as a structured list."""
    
    def _parse_validation_response(self, llm_response: str) -> List[Dict[str, Any]]:
        """Parse LLM validation response."""
        issues = []
        
        try:
            if "{" in llm_response and "}" in llm_response:
                start = llm_response.index("{")
                end = llm_response.rindex("}") + 1
                data = json.loads(llm_response[start:end])
                if "issues" in data:
                    return data["issues"]
        except:
            pass
        
        # Parse text response
        lines = llm_response.split("\n")
        current_issue = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # Detect severity
            severity = "info"
            if "error" in line.lower():
                severity = "error"
            elif "warning" in line.lower():
                severity = "warning"
            
            # Extract issue description
            if line.startswith(("-", "*", "•")) or (line and line[0].isdigit()):
                issue_text = line.lstrip("-*•0123456789. ")
                if issue_text and len(issue_text) > 10:
                    issues.append({
                        "severity": severity,
                        "message": issue_text,
                        "fix": "See LLM suggestions"
                    })
        
        return issues[:10]  # Top 10 issues
    
    async def _auto_fix(
        self,
        spec: WorkflowSpec,
        issues: List[Dict[str, Any]]
    ) -> Optional[WorkflowSpec]:
        """Attempt to automatically fix issues."""
        self.log_action("attempting_auto_fix", workflow_id=spec.id, issue_count=len(issues))
        
        prompt = f"""Given this workflow specification and its issues, provide a corrected version:

**Original Spec**:
{json.dumps({
    'id': spec.id,
    'name': spec.name,
    'description': spec.description,
    'tasks': [{'id': t.id, 'type': t.type, 'params': t.params} for t in spec.tasks]
}, indent=2)}

**Issues**:
{json.dumps(issues, indent=2)}

Provide the corrected workflow specification in valid YAML or JSON format."""
        
        response = await self.think(prompt)
        
        # Try to parse fixed spec
        # In production, this would use proper YAML parsing
        # For now, return None to indicate manual fix needed
        
        self.log_action("auto_fix_attempted", workflow_id=spec.id)
        return None
    
    async def suggest_improvements(self, spec: WorkflowSpec) -> List[str]:
        """Suggest improvements for a valid workflow."""
        prompt = f"""This workflow is valid but could be improved. Suggest enhancements:

**Workflow**: {spec.name}
**Tasks**: {len(spec.tasks)}

Suggest improvements for:
1. Performance
2. Reliability
3. Maintainability
4. Security
5. User experience

Provide 3-5 specific, actionable suggestions."""
        
        response = await self.think(prompt)
        
        # Extract suggestions
        suggestions = []
        lines = response.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith(("-", "*", "•")) or (line and line[0].isdigit()):
                suggestion = line.lstrip("-*•0123456789. ")
                if suggestion and len(suggestion) > 10:
                    suggestions.append(suggestion)
        
        return suggestions[:5]
