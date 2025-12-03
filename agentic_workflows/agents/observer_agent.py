"""
Observer Agent - Monitors workflow execution and collects telemetry.
"""
import time
from typing import Dict, Any, List, Optional
from collections import defaultdict
from .base_agent import BaseAgent
from ..core.audit import AuditLog


class ObserverAgent(BaseAgent):
    """
    Observer agent that monitors workflow execution.
    
    Features:
    - Real-time progress tracking
    - Performance metrics collection
    - Error pattern detection
    - Resource usage monitoring
    - Execution history
    """
    
    def __init__(self, audit: Optional[AuditLog] = None):
        super().__init__(name="ObserverAgent", audit=audit)
        self.workflows: Dict[str, Dict[str, Any]] = {}
        self.metrics: Dict[str, List[float]] = defaultdict(list)
        self.error_patterns: Dict[str, int] = defaultdict(int)
        
    def start_workflow(self, workflow_id: str, metadata: Dict[str, Any]) -> None:
        """Start monitoring a workflow."""
        self.workflows[workflow_id] = {
            "id": workflow_id,
            "start_time": time.time(),
            "end_time": None,
            "status": "running",
            "metadata": metadata,
            "tasks": {},
            "errors": []
        }
        
        self.log_action("workflow_started", {
            "workflow_id": workflow_id,
            "metadata": metadata
        })
        
    def update_task(
        self,
        workflow_id: str,
        task_id: str,
        status: str,
        details: Optional[Dict[str, Any]] = None
    ) -> None:
        """Update task status."""
        if workflow_id not in self.workflows:
            return
            
        workflow = self.workflows[workflow_id]
        
        if task_id not in workflow["tasks"]:
            workflow["tasks"][task_id] = {
                "id": task_id,
                "start_time": time.time(),
                "status": status,
                "updates": []
            }
        else:
            workflow["tasks"][task_id]["status"] = status
            
        if details:
            workflow["tasks"][task_id]["updates"].append({
                "timestamp": time.time(),
                "status": status,
                "details": details
            })
            
        self.log_action("task_updated", {
            "workflow_id": workflow_id,
            "task_id": task_id,
            "status": status
        })
        
    def record_error(
        self,
        workflow_id: str,
        task_id: str,
        error: str,
        error_type: Optional[str] = None
    ) -> None:
        """Record an error."""
        if workflow_id not in self.workflows:
            return
            
        error_entry = {
            "timestamp": time.time(),
            "task_id": task_id,
            "error": error,
            "error_type": error_type or "unknown"
        }
        
        self.workflows[workflow_id]["errors"].append(error_entry)
        
        # Track error patterns
        pattern_key = f"{error_type}:{error[:50]}"
        self.error_patterns[pattern_key] += 1
        
        self.log_action("error_recorded", {
            "workflow_id": workflow_id,
            "task_id": task_id,
            "error_type": error_type
        })
        
    def complete_workflow(
        self,
        workflow_id: str,
        status: str,
        result: Optional[Dict[str, Any]] = None
    ) -> None:
        """Mark workflow as complete."""
        if workflow_id not in self.workflows:
            return
            
        workflow = self.workflows[workflow_id]
        workflow["end_time"] = time.time()
        workflow["status"] = status
        workflow["result"] = result
        
        # Calculate metrics
        duration = workflow["end_time"] - workflow["start_time"]
        self.metrics["workflow_duration"].append(duration)
        self.metrics[f"workflow_{status}"].append(1)
        
        self.log_action("workflow_completed", {
            "workflow_id": workflow_id,
            "status": status,
            "duration": duration,
            "task_count": len(workflow["tasks"]),
            "error_count": len(workflow["errors"])
        })
        
    def get_workflow_status(self, workflow_id: str) -> Optional[Dict[str, Any]]:
        """Get current workflow status."""
        if workflow_id not in self.workflows:
            return None
            
        workflow = self.workflows[workflow_id]
        
        # Calculate progress
        total_tasks = len(workflow["tasks"])
        completed_tasks = sum(
            1 for task in workflow["tasks"].values()
            if task["status"] in ["success", "failed", "skipped"]
        )
        
        progress = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        
        # Calculate duration
        if workflow["end_time"]:
            duration = workflow["end_time"] - workflow["start_time"]
        else:
            duration = time.time() - workflow["start_time"]
            
        return {
            "workflow_id": workflow_id,
            "status": workflow["status"],
            "progress": progress,
            "duration": duration,
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "error_count": len(workflow["errors"]),
            "tasks": workflow["tasks"]
        }
        
    def get_metrics(self) -> Dict[str, Any]:
        """Get aggregated metrics."""
        return {
            "total_workflows": len(self.workflows),
            "active_workflows": sum(
                1 for w in self.workflows.values()
                if w["status"] == "running"
            ),
            "completed_workflows": sum(
                1 for w in self.workflows.values()
                if w["status"] in ["success", "failed"]
            ),
            "average_duration": (
                sum(self.metrics["workflow_duration"]) / len(self.metrics["workflow_duration"])
                if self.metrics["workflow_duration"] else 0
            ),
            "total_errors": sum(self.error_patterns.values()),
            "error_patterns": dict(self.error_patterns),
            "metrics": {k: list(v) for k, v in self.metrics.items()}
        }
        
    def detect_anomalies(self) -> List[Dict[str, Any]]:
        """Detect anomalies in execution patterns."""
        anomalies = []
        
        # Check for high error rate
        if self.metrics["workflow_duration"]:
            error_rate = (
                sum(self.metrics.get("workflow_failed", []))
                / len(self.metrics["workflow_duration"])
            )
            
            if error_rate > 0.3:  # More than 30% failure rate
                anomalies.append({
                    "type": "high_error_rate",
                    "severity": "high",
                    "value": error_rate,
                    "message": f"High failure rate detected: {error_rate:.1%}"
                })
                
        # Check for repeated errors
        for pattern, count in self.error_patterns.items():
            if count > 5:
                anomalies.append({
                    "type": "repeated_error",
                    "severity": "medium",
                    "pattern": pattern,
                    "count": count,
                    "message": f"Error pattern repeated {count} times: {pattern}"
                })
                
        # Check for slow workflows
        if self.metrics["workflow_duration"]:
            avg_duration = sum(self.metrics["workflow_duration"]) / len(self.metrics["workflow_duration"])
            recent_duration = self.metrics["workflow_duration"][-1] if self.metrics["workflow_duration"] else 0
            
            if recent_duration > avg_duration * 2:
                anomalies.append({
                    "type": "slow_execution",
                    "severity": "low",
                    "value": recent_duration,
                    "average": avg_duration,
                    "message": f"Workflow took {recent_duration:.1f}s (avg: {avg_duration:.1f}s)"
                })
                
        return anomalies
        
    def get_recommendations(self) -> List[str]:
        """Get recommendations based on observed patterns."""
        recommendations = []
        
        anomalies = self.detect_anomalies()
        
        for anomaly in anomalies:
            if anomaly["type"] == "high_error_rate":
                recommendations.append(
                    "Consider reviewing failed workflows and adding error handling"
                )
            elif anomaly["type"] == "repeated_error":
                recommendations.append(
                    f"Investigate repeated error pattern: {anomaly['pattern']}"
                )
            elif anomaly["type"] == "slow_execution":
                recommendations.append(
                    "Consider optimizing slow tasks or increasing parallelism"
                )
                
        return recommendations
