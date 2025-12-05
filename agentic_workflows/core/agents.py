from typing import Dict, Any, List
from .spec import WorkflowSpec, TaskSpec
from .audit import AuditLog
from datetime import datetime, timezone
import importlib
import time
import uuid

# Simple factory to resolve plugin classes by name
PLUGIN_REGISTRY = {
    # Core plugins
    "file_organizer": "agentic_workflows.plugins.file_organizer.FileOrganizer",
    "email_summarizer": "agentic_workflows.plugins.email_summarizer.EmailSummarizer",
    "http_task": "agentic_workflows.plugins.http_task.HTTPTask",
    
    # Advanced plugins
    "web_scraper": "agentic_workflows.plugins.advanced.web_scraper.WebScraperPlugin",
    "image_processor": "agentic_workflows.plugins.advanced.image_processor.ImageProcessorPlugin",
    "pdf_extractor": "agentic_workflows.plugins.advanced.pdf_extractor.PDFExtractorPlugin",
    "sql_query": "agentic_workflows.plugins.advanced.sql_query.SQLQueryPlugin",
    "shell_command": "agentic_workflows.plugins.advanced.shell_command.ShellCommandPlugin",
}

def resolve_plugin(type_name: str):
    path = PLUGIN_REGISTRY.get(type_name)
    if not path:
        raise ValueError(f"No plugin registered for type {type_name}")
    module_name, class_name = path.rsplit(".", 1)
    module = importlib.import_module(module_name)
    cls = getattr(module, class_name)
    return cls

def now_iso() -> str:
    """Return current UTC timestamp in ISO format with milliseconds."""
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")

class PlannerAgent:
    def __init__(self, audit: AuditLog = None):
        self.audit = audit or AuditLog()

    def plan(self, spec: WorkflowSpec) -> List[Dict[str, Any]]:
        plan = []
        for t in spec.tasks:
            plan.append({
                "task_id": t.id,
                "type": t.type,
                "params": t.params
            })
        self.audit.record({"agent": "planner", "workflow": spec.id, "plan_size": len(plan)})
        return plan

class ExecutorAgent:
    def __init__(self, audit: AuditLog = None, plugin_overrides: Dict[str, str] = None):
        self.audit = audit or AuditLog()
        self.plugin_overrides = plugin_overrides or {}

    def execute_plan(self, plan: List[Dict[str, Any]], dry_run: bool = True):
        """Execute workflow plan with detailed timing and metadata for each task."""
        results = {}
        overall_start = time.time()
        
        for step in plan:
            task_id = step.get("task_id") or f"task-{uuid.uuid4().hex[:8]}"
            typ = step["type"]
            params = dict(step.get("params", {}))
            params.setdefault("dry_run", dry_run)
            
            # Task-level timing
            task_start_time = time.time()
            task_start_ts = now_iso()
            
            try:
                # Resolve and instantiate plugin
                cls = resolve_plugin(typ)
                plugin = cls(params=params, audit=self.audit)
                
                # Get plan for visibility
                planned_actions = plugin.plan()
                self.audit.record({
                    "agent": "executor",
                    "task_id": task_id,
                    "type": typ,
                    "planned_actions": len(planned_actions),
                    "dry_run": dry_run
                })
                
                if dry_run:
                    # Dry run mode - return plan without execution
                    task_end_ts = now_iso()
                    task_duration = round(time.time() - task_start_time, 3)
                    results[task_id] = {
                        "status": "planned",
                        "type": typ,
                        "plan": planned_actions,
                        "start_ts": task_start_ts,
                        "end_ts": task_end_ts,
                        "duration_seconds": task_duration,
                        "dry_run": True
                    }
                else:
                    # Real execution
                    exec_result = plugin.execute()
                    task_end_ts = now_iso()
                    task_duration = round(time.time() - task_start_time, 3)
                    
                    # Normalize plugin output
                    if isinstance(exec_result, dict):
                        status = exec_result.get("status", "completed")
                        result_data = exec_result
                    else:
                        status = "completed"
                        result_data = {"output": str(exec_result)}
                    
                    results[task_id] = {
                        "status": status,
                        "type": typ,
                        "result": result_data,
                        "start_ts": task_start_ts,
                        "end_ts": task_end_ts,
                        "duration_seconds": task_duration,
                        "dry_run": False
                    }
                    
                    self.audit.record({
                        "agent": "executor",
                        "task_id": task_id,
                        "status": status,
                        "duration": task_duration
                    })
                    
            except Exception as e:
                task_end_ts = now_iso()
                task_duration = round(time.time() - task_start_time, 3)
                error_msg = str(e)
                
                self.audit.record({
                    "agent": "executor",
                    "task_id": task_id,
                    "error": error_msg,
                    "duration": task_duration
                })
                
                results[task_id] = {
                    "status": "failed",
                    "type": typ,
                    "error": error_msg,
                    "start_ts": task_start_ts,
                    "end_ts": task_end_ts,
                    "duration_seconds": task_duration,
                    "dry_run": dry_run
                }
        
        overall_duration = round(time.time() - overall_start, 3)
        
        return {
            "results": results,
            "overall_duration_seconds": overall_duration,
            "tasks_total": len(plan),
            "tasks_completed": sum(1 for r in results.values() if r.get("status") in ("completed", "planned")),
            "tasks_failed": sum(1 for r in results.values() if r.get("status") == "failed")
        }
