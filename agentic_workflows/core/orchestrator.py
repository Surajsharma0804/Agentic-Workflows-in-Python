from .spec import load_spec
from .agents import PlannerAgent, ExecutorAgent, now_iso
from .audit import AuditLog
from datetime import datetime, timezone
import time
import uuid
import platform
import os

class Orchestrator:
    def __init__(self, audit_path="audit.log"):
        self.audit = AuditLog(audit_path)
        self.planner = PlannerAgent(audit=self.audit)
        self.executor = ExecutorAgent(audit=self.audit)

    def run_spec(self, spec_path: str, dry_run: bool = True):
        """
        Execute a workflow specification with full timing, metadata, and unique identifiers.
        
        Returns a production-ready response with:
        - Unique workflow_id for each run
        - Start/end timestamps with millisecond precision
        - Numeric duration in seconds
        - Per-task timing and results
        - Run metadata (environment, host, etc.)
        """
        # Generate unique run ID
        run_id = f"wf_{uuid.uuid4().hex}"
        
        # Timing
        start_time = time.time()
        start_ts = now_iso()
        
        # Load and plan
        spec = load_spec(spec_path)
        plan = self.planner.plan(spec)
        
        # Audit start
        self.audit.record({
            "orchestrator": "starting_run",
            "workflow_id": run_id,
            "spec": spec_path,
            "spec_name": spec.name,
            "dry_run": dry_run,
            "tasks_count": len(plan)
        })
        
        # Execute plan
        exec_output = self.executor.execute_plan(plan, dry_run=dry_run)
        
        # Timing
        end_time = time.time()
        end_ts = now_iso()
        total_duration = round(end_time - start_time, 3)
        
        # Compute status
        results = exec_output.get("results", {})
        all_success = all(
            r.get("status") in ("completed", "planned") 
            for r in results.values()
        )
        status = "success" if all_success else "partial_failure"
        
        # Build response with rich metadata
        response = {
            "status": status,
            "workflow_id": run_id,
            "workflow_name": spec.name,
            "spec_path": spec_path,
            "dry_run": dry_run,
            
            # Timing
            "start_timestamp": start_ts,
            "end_timestamp": end_ts,
            "duration_seconds": total_duration,
            
            # Task summary
            "tasks_total": exec_output.get("tasks_total", len(plan)),
            "tasks_completed": exec_output.get("tasks_completed", 0),
            "tasks_failed": exec_output.get("tasks_failed", 0),
            
            # Detailed results
            "results": results,
            
            # Metadata
            "metadata": {
                "executor_duration_seconds": exec_output.get("overall_duration_seconds", 0),
                "platform": platform.system(),
                "python_version": platform.python_version(),
                "hostname": platform.node(),
                "environment": os.getenv("ENVIRONMENT", "development")
            }
        }
        
        # Audit completion
        self.audit.record({
            "orchestrator": "run_complete",
            "workflow_id": run_id,
            "spec": spec_path,
            "status": status,
            "duration": total_duration,
            "tasks_completed": response["tasks_completed"],
            "tasks_failed": response["tasks_failed"]
        })
        
        return response
