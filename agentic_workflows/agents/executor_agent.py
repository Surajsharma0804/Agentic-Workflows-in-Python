"""
Async Executor Agent - Executes workflow tasks with DAG support.
"""
import asyncio
from typing import Dict, Any, List, Optional
from .base_agent import BaseAgent
from ..dag.dag_engine import DAGEngine, DAGNode
from ..core.agents import resolve_plugin
from ..core.audit import AuditLog


class ExecutorAgent(BaseAgent):
    """
    Async executor agent that runs workflow tasks using DAG engine.
    
    Features:
    - Parallel execution of independent tasks
    - Dependency resolution
    - Plugin isolation
    - Real-time progress tracking
    - Graceful error handling
    """
    
    def __init__(
        self,
        audit: Optional[AuditLog] = None,
        max_concurrent: int = 10,
        dry_run: bool = False
    ):
        super().__init__(name="ExecutorAgent", audit=audit)
        self.max_concurrent = max_concurrent
        self.dry_run = dry_run
        self.dag_engine: Optional[DAGEngine] = None
        
    async def execute_workflow(
        self,
        tasks: List[Dict[str, Any]],
        fail_fast: bool = False
    ) -> Dict[str, Any]:
        """
        Execute a workflow using DAG engine.
        
        Args:
            tasks: List of task specifications
            fail_fast: Stop on first failure
            
        Returns:
            Execution result with status and details
        """
        self.log_action("execute_workflow", {
            "task_count": len(tasks),
            "dry_run": self.dry_run,
            "fail_fast": fail_fast
        })
        
        # Build DAG from tasks
        self.dag_engine = DAGEngine(
            audit=self.audit,
            max_concurrent=self.max_concurrent
        )
        self.dag_engine.build_from_spec(tasks)
        
        # Execute DAG
        result = await self.dag_engine.execute(
            executor_func=self._execute_node,
            fail_fast=fail_fast
        )
        
        return {
            "success": result.success,
            "total_duration": result.total_duration,
            "successful_nodes": result.successful_nodes,
            "failed_nodes": result.failed_nodes,
            "skipped_nodes": result.skipped_nodes,
            "node_details": {
                node_id: {
                    "status": node.status.value,
                    "duration": node.duration,
                    "result": node.result,
                    "error": node.error,
                    "retry_count": node.retry_count
                }
                for node_id, node in result.nodes.items()
            }
        }
        
    async def _execute_node(self, node: DAGNode) -> Any:
        """
        Execute a single DAG node by resolving and running the plugin.
        
        Args:
            node: DAG node to execute
            
        Returns:
            Execution result
        """
        self.log_action("execute_node", {
            "node_id": node.id,
            "task_type": node.task_type
        })
        
        try:
            # Resolve plugin
            plugin_class = resolve_plugin(node.task_type)
            
            # Prepare params
            params = dict(node.params)
            params["dry_run"] = self.dry_run
            
            # Create plugin instance
            plugin = plugin_class(params=params, audit=self.audit)
            
            # Get execution plan
            plan = plugin.plan()
            self.log_action("node_plan", {
                "node_id": node.id,
                "planned_actions": len(plan)
            })
            
            if self.dry_run:
                return {
                    "status": "planned",
                    "plan": plan,
                    "dry_run": True
                }
                
            # Execute plugin
            result = plugin.execute()
            
            self.log_action("node_complete", {
                "node_id": node.id,
                "status": result.get("status", "success")
            })
            
            return result
            
        except Exception as e:
            self.log_action("node_error", {
                "node_id": node.id,
                "error": str(e)
            })
            raise
            
    def get_status(self) -> Dict[str, Any]:
        """Get current execution status."""
        if not self.dag_engine:
            return {"status": "not_started"}
            
        return self.dag_engine.get_status()
        
    async def execute_single_task(
        self,
        task_type: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute a single task without DAG.
        
        Args:
            task_type: Type of task/plugin
            params: Task parameters
            
        Returns:
            Execution result
        """
        self.log_action("execute_single_task", {
            "task_type": task_type
        })
        
        try:
            # Resolve plugin
            plugin_class = resolve_plugin(task_type)
            
            # Prepare params
            task_params = dict(params)
            task_params["dry_run"] = self.dry_run
            
            # Create and execute plugin
            plugin = plugin_class(params=task_params, audit=self.audit)
            result = plugin.execute()
            
            return {
                "success": True,
                "result": result
            }
            
        except Exception as e:
            self.log_action("task_error", {
                "task_type": task_type,
                "error": str(e)
            })
            return {
                "success": False,
                "error": str(e)
            }
