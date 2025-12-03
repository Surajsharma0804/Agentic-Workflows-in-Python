"""
DAG (Directed Acyclic Graph) Execution Engine
Supports parallel execution, dependencies, retries, and async operations.
"""
import asyncio
from typing import Dict, List, Any, Optional, Set, Callable
from dataclasses import dataclass, field
from enum import Enum
import time
from ..core.audit import AuditLog
from ..core.exceptions import WorkflowExecutionError


class NodeStatus(Enum):
    """Status of a DAG node during execution."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class DAGNode:
    """Represents a node in the DAG."""
    id: str
    task_type: str
    params: Dict[str, Any]
    dependencies: List[str] = field(default_factory=list)
    status: NodeStatus = NodeStatus.PENDING
    result: Optional[Any] = None
    error: Optional[str] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    retry_count: int = 0
    max_retries: int = 3
    
    @property
    def duration(self) -> Optional[float]:
        """Calculate execution duration."""
        if self.start_time and self.end_time:
            return self.end_time - self.start_time
        return None


@dataclass
class DAGExecutionResult:
    """Result of DAG execution."""
    success: bool
    nodes: Dict[str, DAGNode]
    total_duration: float
    failed_nodes: List[str]
    successful_nodes: List[str]
    skipped_nodes: List[str]


class DAGEngine:
    """
    Async DAG execution engine with parallel execution support.
    
    Features:
    - Parallel execution of independent tasks
    - Dependency resolution
    - Automatic retries with exponential backoff
    - Graceful error handling
    - Real-time progress tracking
    """
    
    def __init__(
        self,
        audit: Optional[AuditLog] = None,
        max_concurrent: int = 10,
        default_timeout: int = 300
    ):
        self.audit = audit or AuditLog()
        self.max_concurrent = max_concurrent
        self.default_timeout = default_timeout
        self.nodes: Dict[str, DAGNode] = {}
        self.execution_order: List[List[str]] = []
        
    def add_node(self, node: DAGNode) -> None:
        """Add a node to the DAG."""
        if node.id in self.nodes:
            raise ValueError(f"Node {node.id} already exists")
        self.nodes[node.id] = node
        
    def build_from_spec(self, tasks: List[Dict[str, Any]]) -> None:
        """Build DAG from workflow specification."""
        for task in tasks:
            node = DAGNode(
                id=task.get("id", task.get("task_id", f"task_{len(self.nodes)}")),
                task_type=task.get("type", "unknown"),
                params=task.get("params", {}),
                dependencies=task.get("depends_on", []),
                max_retries=task.get("max_retries", 3)
            )
            self.add_node(node)
            
    def validate_dag(self) -> bool:
        """Validate DAG structure (no cycles, valid dependencies)."""
        # Check for cycles using DFS
        visited = set()
        rec_stack = set()
        
        def has_cycle(node_id: str) -> bool:
            visited.add(node_id)
            rec_stack.add(node_id)
            
            node = self.nodes.get(node_id)
            if not node:
                return False
                
            for dep in node.dependencies:
                if dep not in visited:
                    if has_cycle(dep):
                        return True
                elif dep in rec_stack:
                    return True
                    
            rec_stack.remove(node_id)
            return False
            
        for node_id in self.nodes:
            if node_id not in visited:
                if has_cycle(node_id):
                    raise WorkflowExecutionError(f"Cycle detected in DAG at node {node_id}")
                    
        # Validate all dependencies exist
        for node_id, node in self.nodes.items():
            for dep in node.dependencies:
                if dep not in self.nodes:
                    raise WorkflowExecutionError(
                        f"Node {node_id} depends on non-existent node {dep}"
                    )
                    
        return True
        
    def compute_execution_order(self) -> List[List[str]]:
        """
        Compute execution order using topological sort.
        Returns list of levels where each level can be executed in parallel.
        """
        # Calculate in-degree for each node
        in_degree = {node_id: 0 for node_id in self.nodes}
        for node in self.nodes.values():
            for dep in node.dependencies:
                in_degree[node.id] += 1
                
        # Find nodes with no dependencies (level 0)
        levels = []
        remaining = set(self.nodes.keys())
        
        while remaining:
            # Find all nodes with no remaining dependencies
            current_level = [
                node_id for node_id in remaining
                if all(dep not in remaining for dep in self.nodes[node_id].dependencies)
            ]
            
            if not current_level:
                raise WorkflowExecutionError("Cannot compute execution order - possible cycle")
                
            levels.append(current_level)
            remaining -= set(current_level)
            
        self.execution_order = levels
        return levels
        
    async def execute_node(
        self,
        node_id: str,
        executor_func: Callable[[DAGNode], Any]
    ) -> None:
        """Execute a single node with retry logic."""
        node = self.nodes[node_id]
        node.status = NodeStatus.RUNNING
        node.start_time = time.time()
        
        self.audit.record({
            "event": "node_start",
            "node_id": node_id,
            "task_type": node.task_type
        })
        
        while node.retry_count <= node.max_retries:
            try:
                # Execute the node
                result = await asyncio.wait_for(
                    executor_func(node),
                    timeout=self.default_timeout
                )
                
                node.result = result
                node.status = NodeStatus.SUCCESS
                node.end_time = time.time()
                
                self.audit.record({
                    "event": "node_success",
                    "node_id": node_id,
                    "duration": node.duration,
                    "retry_count": node.retry_count
                })
                return
                
            except asyncio.TimeoutError:
                error_msg = f"Node {node_id} timed out after {self.default_timeout}s"
                node.error = error_msg
                node.retry_count += 1
                
                if node.retry_count > node.max_retries:
                    node.status = NodeStatus.FAILED
                    node.end_time = time.time()
                    self.audit.record({
                        "event": "node_failed",
                        "node_id": node_id,
                        "error": error_msg,
                        "retry_count": node.retry_count
                    })
                    raise
                    
                # Exponential backoff
                await asyncio.sleep(2 ** node.retry_count)
                
            except Exception as e:
                error_msg = str(e)
                node.error = error_msg
                node.retry_count += 1
                
                if node.retry_count > node.max_retries:
                    node.status = NodeStatus.FAILED
                    node.end_time = time.time()
                    self.audit.record({
                        "event": "node_failed",
                        "node_id": node_id,
                        "error": error_msg,
                        "retry_count": node.retry_count
                    })
                    raise
                    
                # Exponential backoff
                await asyncio.sleep(2 ** node.retry_count)
                
    async def execute(
        self,
        executor_func: Callable[[DAGNode], Any],
        fail_fast: bool = False
    ) -> DAGExecutionResult:
        """
        Execute the DAG with parallel execution of independent nodes.
        
        Args:
            executor_func: Async function that executes a node
            fail_fast: If True, stop execution on first failure
            
        Returns:
            DAGExecutionResult with execution details
        """
        start_time = time.time()
        
        # Validate and compute execution order
        self.validate_dag()
        self.compute_execution_order()
        
        self.audit.record({
            "event": "dag_start",
            "total_nodes": len(self.nodes),
            "execution_levels": len(self.execution_order)
        })
        
        failed_nodes = []
        successful_nodes = []
        skipped_nodes = []
        
        # Execute level by level
        for level_idx, level in enumerate(self.execution_order):
            self.audit.record({
                "event": "level_start",
                "level": level_idx,
                "nodes": level
            })
            
            # Check if any dependencies failed
            nodes_to_execute = []
            for node_id in level:
                node = self.nodes[node_id]
                
                # Check if any dependency failed
                failed_deps = [
                    dep for dep in node.dependencies
                    if self.nodes[dep].status == NodeStatus.FAILED
                ]
                
                if failed_deps:
                    node.status = NodeStatus.SKIPPED
                    node.error = f"Dependencies failed: {failed_deps}"
                    skipped_nodes.append(node_id)
                    self.audit.record({
                        "event": "node_skipped",
                        "node_id": node_id,
                        "reason": "failed_dependencies"
                    })
                else:
                    nodes_to_execute.append(node_id)
                    
            if not nodes_to_execute:
                continue
                
            # Execute nodes in parallel with concurrency limit
            semaphore = asyncio.Semaphore(self.max_concurrent)
            
            async def execute_with_semaphore(node_id: str):
                async with semaphore:
                    try:
                        await self.execute_node(node_id, executor_func)
                        successful_nodes.append(node_id)
                    except Exception as e:
                        failed_nodes.append(node_id)
                        if fail_fast:
                            raise
                            
            # Execute all nodes in this level
            tasks = [execute_with_semaphore(node_id) for node_id in nodes_to_execute]
            
            if fail_fast:
                await asyncio.gather(*tasks)
            else:
                await asyncio.gather(*tasks, return_exceptions=True)
                
            # Check if we should stop
            if fail_fast and failed_nodes:
                # Mark remaining nodes as skipped
                for remaining_level in self.execution_order[level_idx + 1:]:
                    for node_id in remaining_level:
                        self.nodes[node_id].status = NodeStatus.SKIPPED
                        skipped_nodes.append(node_id)
                break
                
        total_duration = time.time() - start_time
        success = len(failed_nodes) == 0
        
        self.audit.record({
            "event": "dag_complete",
            "success": success,
            "duration": total_duration,
            "successful": len(successful_nodes),
            "failed": len(failed_nodes),
            "skipped": len(skipped_nodes)
        })
        
        return DAGExecutionResult(
            success=success,
            nodes=self.nodes,
            total_duration=total_duration,
            failed_nodes=failed_nodes,
            successful_nodes=successful_nodes,
            skipped_nodes=skipped_nodes
        )
        
    def get_status(self) -> Dict[str, Any]:
        """Get current execution status."""
        return {
            "total_nodes": len(self.nodes),
            "pending": sum(1 for n in self.nodes.values() if n.status == NodeStatus.PENDING),
            "running": sum(1 for n in self.nodes.values() if n.status == NodeStatus.RUNNING),
            "success": sum(1 for n in self.nodes.values() if n.status == NodeStatus.SUCCESS),
            "failed": sum(1 for n in self.nodes.values() if n.status == NodeStatus.FAILED),
            "skipped": sum(1 for n in self.nodes.values() if n.status == NodeStatus.SKIPPED),
            "nodes": {
                node_id: {
                    "status": node.status.value,
                    "duration": node.duration,
                    "retry_count": node.retry_count
                }
                for node_id, node in self.nodes.items()
            }
        }
