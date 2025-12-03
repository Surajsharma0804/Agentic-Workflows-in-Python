"""Planner Agent - Converts workflow specs to execution plans using LLM."""
from typing import Dict, Any, List, Optional
import json
import structlog

from .base_agent import BaseAgent
from ..core.spec import WorkflowSpec

logger = structlog.get_logger()


class PlannerAgent(BaseAgent):
    """AI-powered workflow planner."""
    
    def get_system_prompt(self) -> str:
        return """You are an expert workflow planning AI assistant. Your role is to:

1. Analyze workflow specifications
2. Identify optimal task execution order
3. Detect parallelization opportunities
4. Suggest improvements and optimizations
5. Validate dependencies and prerequisites

Provide clear, actionable execution plans in a structured format."""
    
    def fallback_response(self, prompt: str) -> str:
        return json.dumps({
            "plan": "sequential",
            "tasks": [],
            "notes": "Using fallback sequential execution plan"
        })
    
    async def plan_workflow(self, spec: WorkflowSpec) -> Dict[str, Any]:
        """
        Create an intelligent execution plan for a workflow.
        
        Args:
            spec: Workflow specification
        
        Returns:
            Execution plan with task ordering, parallelization, and optimizations
        """
        self.log_action("planning_workflow", workflow_id=spec.id, task_count=len(spec.tasks))
        
        # Build prompt with workflow details
        prompt = self._build_planning_prompt(spec)
        
        # Get LLM suggestions
        llm_response = await self.think(prompt)
        
        # Parse and structure the plan
        plan = self._parse_plan(llm_response, spec)
        
        self.log_action("plan_created", workflow_id=spec.id, plan_type=plan.get("execution_strategy"))
        
        return plan
    
    def _build_planning_prompt(self, spec: WorkflowSpec) -> str:
        """Build prompt for workflow planning."""
        tasks_desc = "\n".join([
            f"- Task {i+1}: {task.id} (type: {task.type})"
            for i, task in enumerate(spec.tasks)
        ])
        
        return f"""Analyze this workflow and create an optimal execution plan:

**Workflow**: {spec.name}
**Description**: {spec.description}

**Tasks**:
{tasks_desc}

**Total Tasks**: {len(spec.tasks)}

Please provide:
1. Recommended execution strategy (sequential, parallel, or hybrid)
2. Task grouping for parallel execution
3. Estimated execution time
4. Potential risks or bottlenecks
5. Optimization suggestions

Format your response as a structured plan."""
    
    def _parse_plan(self, llm_response: str, spec: WorkflowSpec) -> Dict[str, Any]:
        """Parse LLM response into structured plan."""
        # Try to extract JSON if present
        try:
            if "{" in llm_response and "}" in llm_response:
                start = llm_response.index("{")
                end = llm_response.rindex("}") + 1
                plan_data = json.loads(llm_response[start:end])
                return plan_data
        except:
            pass
        
        # Fallback: Create structured plan from spec
        return {
            "workflow_id": spec.id,
            "execution_strategy": self._detect_strategy(llm_response),
            "task_order": [task.id for task in spec.tasks],
            "parallel_groups": self._detect_parallel_groups(llm_response, spec),
            "estimated_duration": "unknown",
            "llm_suggestions": llm_response,
            "risks": self._extract_risks(llm_response),
            "optimizations": self._extract_optimizations(llm_response)
        }
    
    def _detect_strategy(self, response: str) -> str:
        """Detect execution strategy from LLM response."""
        response_lower = response.lower()
        if "parallel" in response_lower:
            return "parallel"
        elif "hybrid" in response_lower:
            return "hybrid"
        return "sequential"
    
    def _detect_parallel_groups(self, response: str, spec: WorkflowSpec) -> List[List[str]]:
        """Detect which tasks can run in parallel."""
        # Simple heuristic: tasks with no dependencies can run in parallel
        # In production, this would use dependency analysis
        return [[task.id] for task in spec.tasks]
    
    def _extract_risks(self, response: str) -> List[str]:
        """Extract risks from LLM response."""
        risks = []
        lines = response.split("\n")
        for line in lines:
            if "risk" in line.lower() or "warning" in line.lower():
                risks.append(line.strip())
        return risks[:5]  # Top 5 risks
    
    def _extract_optimizations(self, response: str) -> List[str]:
        """Extract optimization suggestions from LLM response."""
        optimizations = []
        lines = response.split("\n")
        for line in lines:
            if "optim" in line.lower() or "improve" in line.lower() or "suggest" in line.lower():
                optimizations.append(line.strip())
        return optimizations[:5]  # Top 5 suggestions
    
    async def explain_plan(self, plan: Dict[str, Any]) -> str:
        """Generate human-friendly explanation of the plan."""
        prompt = f"""Explain this workflow execution plan in simple terms:

{json.dumps(plan, indent=2)}

Provide a clear, concise explanation that a non-technical user can understand."""
        
        return await self.think(prompt)
