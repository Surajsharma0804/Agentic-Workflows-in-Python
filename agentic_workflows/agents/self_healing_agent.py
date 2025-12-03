"""
Self-Healing Agent - Automatically attempts to fix failed workflows.
"""
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
from .recovery_agent import RecoveryAgent
from ..core.audit import AuditLog
from ..llm.factory import get_llm_provider


class SelfHealingAgent(BaseAgent):
    """
    Self-healing agent that automatically attempts to fix failed workflows.
    
    Features:
    - Automatic error analysis
    - Recovery strategy generation
    - Safe remediation attempts
    - Learning from past fixes
    - Human-in-the-loop for critical actions
    """
    
    def __init__(
        self,
        audit: Optional[AuditLog] = None,
        llm_provider: Optional[str] = None,
        auto_fix_enabled: bool = False
    ):
        super().__init__(name="SelfHealingAgent", audit=audit)
        self.recovery_agent = RecoveryAgent(audit=audit, llm_provider=llm_provider)
        self.auto_fix_enabled = auto_fix_enabled
        self.fix_history: List[Dict[str, Any]] = []
        self.learned_patterns: Dict[str, Dict[str, Any]] = {}
        
    async def analyze_failure(
        self,
        workflow_id: str,
        task_id: str,
        error: str,
        context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze a workflow failure and determine if it can be auto-fixed.
        
        Args:
            workflow_id: Workflow identifier
            task_id: Failed task identifier
            error: Error message
            context: Execution context
            
        Returns:
            Analysis result with fix suggestions
        """
        self.log_action("analyze_failure", {
            "workflow_id": workflow_id,
            "task_id": task_id,
            "error": error[:100]
        })
        
        # Check if we've seen this error before
        error_signature = self._get_error_signature(error)
        learned_fix = self.learned_patterns.get(error_signature)
        
        if learned_fix:
            self.log_action("learned_fix_found", {
                "error_signature": error_signature,
                "success_rate": learned_fix.get("success_rate", 0)
            })
            
            return {
                "can_auto_fix": learned_fix["success_rate"] > 0.7,
                "fix_strategy": learned_fix["strategy"],
                "confidence": learned_fix["success_rate"],
                "source": "learned"
            }
            
        # Use recovery agent to generate fix
        recovery_result = await self.recovery_agent.suggest_recovery(
            error_message=error,
            task_context=context
        )
        
        return {
            "can_auto_fix": self._is_safe_to_auto_fix(recovery_result),
            "fix_strategy": recovery_result.get("suggestions", []),
            "confidence": recovery_result.get("confidence", 0),
            "source": "generated"
        }
        
    async def attempt_fix(
        self,
        workflow_id: str,
        task_id: str,
        fix_strategy: Dict[str, Any],
        require_approval: bool = True
    ) -> Dict[str, Any]:
        """
        Attempt to fix a failed workflow.
        
        Args:
            workflow_id: Workflow identifier
            task_id: Failed task identifier
            fix_strategy: Fix strategy to apply
            require_approval: Whether to require human approval
            
        Returns:
            Fix result
        """
        self.log_action("attempt_fix", {
            "workflow_id": workflow_id,
            "task_id": task_id,
            "require_approval": require_approval
        })
        
        if require_approval and not self.auto_fix_enabled:
            return {
                "status": "pending_approval",
                "message": "Fix requires human approval",
                "fix_strategy": fix_strategy
            }
            
        try:
            # Apply fix (implementation depends on fix type)
            result = await self._apply_fix(workflow_id, task_id, fix_strategy)
            
            # Record fix attempt
            fix_record = {
                "workflow_id": workflow_id,
                "task_id": task_id,
                "fix_strategy": fix_strategy,
                "result": result,
                "success": result.get("success", False)
            }
            self.fix_history.append(fix_record)
            
            # Learn from this fix
            if result.get("success"):
                self._learn_from_fix(fix_strategy, success=True)
                
            return result
            
        except Exception as e:
            self.log_action("fix_failed", {
                "workflow_id": workflow_id,
                "error": str(e)
            })
            
            self._learn_from_fix(fix_strategy, success=False)
            
            return {
                "status": "failed",
                "error": str(e)
            }
            
    async def _apply_fix(
        self,
        workflow_id: str,
        task_id: str,
        fix_strategy: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Apply a fix strategy (placeholder for actual implementation)."""
        # This would contain actual fix logic based on strategy type
        # For now, return a simulated result
        
        strategy_type = fix_strategy.get("type", "unknown")
        
        if strategy_type == "retry_with_backoff":
            return {
                "success": True,
                "message": "Task retried successfully with exponential backoff"
            }
        elif strategy_type == "adjust_parameters":
            return {
                "success": True,
                "message": "Task parameters adjusted and retried"
            }
        elif strategy_type == "skip_task":
            return {
                "success": True,
                "message": "Task skipped, workflow continued"
            }
        else:
            return {
                "success": False,
                "message": f"Unknown fix strategy: {strategy_type}"
            }
            
    def _get_error_signature(self, error: str) -> str:
        """Generate a signature for an error to match against learned patterns."""
        # Simple signature based on error type and first few words
        words = error.lower().split()[:5]
        return "_".join(words)
        
    def _is_safe_to_auto_fix(self, recovery_result: Dict[str, Any]) -> bool:
        """Determine if a fix is safe to apply automatically."""
        # Only auto-fix if:
        # 1. Confidence is high
        # 2. Fix doesn't involve destructive operations
        # 3. Fix is a known safe pattern
        
        confidence = recovery_result.get("confidence", 0)
        suggestions = recovery_result.get("suggestions", [])
        
        if confidence < 0.8:
            return False
            
        # Check for destructive operations
        destructive_keywords = ["delete", "remove", "drop", "truncate"]
        for suggestion in suggestions:
            suggestion_text = str(suggestion).lower()
            if any(keyword in suggestion_text for keyword in destructive_keywords):
                return False
                
        return True
        
    def _learn_from_fix(self, fix_strategy: Dict[str, Any], success: bool) -> None:
        """Learn from a fix attempt to improve future recommendations."""
        strategy_signature = str(fix_strategy.get("type", "unknown"))
        
        if strategy_signature not in self.learned_patterns:
            self.learned_patterns[strategy_signature] = {
                "strategy": fix_strategy,
                "attempts": 0,
                "successes": 0,
                "success_rate": 0.0
            }
            
        pattern = self.learned_patterns[strategy_signature]
        pattern["attempts"] += 1
        
        if success:
            pattern["successes"] += 1
            
        pattern["success_rate"] = pattern["successes"] / pattern["attempts"]
        
        self.log_action("learned_pattern_updated", {
            "strategy": strategy_signature,
            "success_rate": pattern["success_rate"],
            "attempts": pattern["attempts"]
        })
        
    def get_fix_history(self) -> List[Dict[str, Any]]:
        """Get history of fix attempts."""
        return self.fix_history
        
    def get_learned_patterns(self) -> Dict[str, Dict[str, Any]]:
        """Get learned fix patterns."""
        return self.learned_patterns
        
    def get_statistics(self) -> Dict[str, Any]:
        """Get self-healing statistics."""
        total_attempts = len(self.fix_history)
        successful_fixes = sum(1 for fix in self.fix_history if fix.get("result", {}).get("success"))
        
        return {
            "total_fix_attempts": total_attempts,
            "successful_fixes": successful_fixes,
            "success_rate": successful_fixes / total_attempts if total_attempts > 0 else 0,
            "learned_patterns": len(self.learned_patterns),
            "auto_fix_enabled": self.auto_fix_enabled
        }
