"""Recovery Agent - Suggests fixes for failed tasks using LLM."""
from typing import Dict, Any, List, Optional
import json
import structlog

from .base_agent import BaseAgent

logger = structlog.get_logger()


class RecoveryAgent(BaseAgent):
    """AI-powered error recovery agent."""
    
    def get_system_prompt(self) -> str:
        return """You are an expert error recovery AI assistant. Your role is to:

1. Analyze task failures and error messages
2. Identify root causes
3. Suggest specific recovery actions
4. Provide step-by-step remediation plans
5. Recommend preventive measures

Be specific, actionable, and prioritize safety."""
    
    def fallback_response(self, prompt: str) -> str:
        return json.dumps({
            "recovery_strategy": "retry",
            "actions": ["Retry the task with same parameters"],
            "confidence": "low"
        })
    
    async def analyze_failure(
        self,
        task_id: str,
        error_message: str,
        task_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze a task failure and suggest recovery actions.
        
        Args:
            task_id: Failed task ID
            error_message: Error message
            task_context: Task configuration and state
        
        Returns:
            Recovery plan with suggested actions
        """
        self.log_action("analyzing_failure", task_id=task_id)
        
        prompt = self._build_recovery_prompt(task_id, error_message, task_context)
        llm_response = await self.think(prompt)
        
        recovery_plan = self._parse_recovery_plan(llm_response)
        recovery_plan["task_id"] = task_id
        recovery_plan["original_error"] = error_message
        
        self.log_action(
            "recovery_plan_created",
            task_id=task_id,
            strategy=recovery_plan.get("recovery_strategy")
        )
        
        return recovery_plan
    
    def _build_recovery_prompt(
        self,
        task_id: str,
        error_message: str,
        task_context: Dict[str, Any]
    ) -> str:
        """Build prompt for error recovery analysis."""
        return f"""Analyze this task failure and suggest recovery actions:

**Task ID**: {task_id}
**Task Type**: {task_context.get('type', 'unknown')}
**Error Message**: {error_message}

**Task Configuration**:
{json.dumps(task_context.get('params', {}), indent=2)}

**Execution Context**:
- Attempt: {task_context.get('attempt', 1)}
- Previous attempts: {task_context.get('previous_attempts', 0)}

Please provide:
1. Root cause analysis
2. Recommended recovery strategy (retry, skip, modify, manual)
3. Specific actions to take
4. Modified parameters if needed
5. Confidence level (high/medium/low)
6. Preventive measures for future runs

Be specific and actionable."""
    
    def _parse_recovery_plan(self, llm_response: str) -> Dict[str, Any]:
        """Parse LLM response into structured recovery plan."""
        try:
            if "{" in llm_response and "}" in llm_response:
                start = llm_response.index("{")
                end = llm_response.rindex("}") + 1
                return json.loads(llm_response[start:end])
        except:
            pass
        
        # Extract key information from text response
        return {
            "recovery_strategy": self._extract_strategy(llm_response),
            "root_cause": self._extract_root_cause(llm_response),
            "actions": self._extract_actions(llm_response),
            "modified_params": {},
            "confidence": self._extract_confidence(llm_response),
            "preventive_measures": self._extract_preventive_measures(llm_response),
            "llm_analysis": llm_response
        }
    
    def _extract_strategy(self, response: str) -> str:
        """Extract recovery strategy from response."""
        response_lower = response.lower()
        if "retry" in response_lower:
            return "retry"
        elif "skip" in response_lower:
            return "skip"
        elif "modify" in response_lower or "adjust" in response_lower:
            return "modify"
        elif "manual" in response_lower:
            return "manual"
        return "unknown"
    
    def _extract_root_cause(self, response: str) -> str:
        """Extract root cause from response."""
        lines = response.split("\n")
        for i, line in enumerate(lines):
            if "root cause" in line.lower() or "cause:" in line.lower():
                # Return next line or same line after colon
                if ":" in line:
                    return line.split(":", 1)[1].strip()
                elif i + 1 < len(lines):
                    return lines[i + 1].strip()
        return "Unknown"
    
    def _extract_actions(self, response: str) -> List[str]:
        """Extract action items from response."""
        actions = []
        lines = response.split("\n")
        for line in lines:
            line = line.strip()
            if line.startswith(("-", "*", "•")) or (line and line[0].isdigit() and "." in line[:3]):
                action = line.lstrip("-*•0123456789. ")
                if action and len(action) > 10:
                    actions.append(action)
        return actions[:5]  # Top 5 actions
    
    def _extract_confidence(self, response: str) -> str:
        """Extract confidence level from response."""
        response_lower = response.lower()
        if "high confidence" in response_lower or "confident" in response_lower:
            return "high"
        elif "low confidence" in response_lower or "uncertain" in response_lower:
            return "low"
        return "medium"
    
    def _extract_preventive_measures(self, response: str) -> List[str]:
        """Extract preventive measures from response."""
        measures = []
        lines = response.split("\n")
        in_preventive_section = False
        
        for line in lines:
            if "preventive" in line.lower() or "prevent" in line.lower():
                in_preventive_section = True
                continue
            
            if in_preventive_section:
                line = line.strip()
                if line.startswith(("-", "*", "•")) or (line and line[0].isdigit()):
                    measure = line.lstrip("-*•0123456789. ")
                    if measure and len(measure) > 10:
                        measures.append(measure)
        
        return measures[:3]  # Top 3 measures
    
    async def suggest_alternative_approach(
        self,
        task_id: str,
        failed_approach: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Suggest alternative approach for a failed task."""
        prompt = f"""The following approach failed:

**Task**: {task_id}
**Failed Approach**: {json.dumps(failed_approach, indent=2)}

Suggest an alternative approach that might succeed. Be creative but practical."""
        
        response = await self.think(prompt)
        
        return {
            "task_id": task_id,
            "alternative_approach": response,
            "confidence": "medium"
        }
