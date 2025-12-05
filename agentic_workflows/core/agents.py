from typing import Dict, Any, List
from .spec import WorkflowSpec, TaskSpec
from .audit import AuditLog
import importlib

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
        results = []
        for step in plan:
            typ = step["type"]
            params = dict(step.get("params", {}))
            params.setdefault("dry_run", dry_run)
            # resolve plugin
            cls = resolve_plugin(typ)
            plugin = cls(params=params, audit=self.audit)
            # get high-level plan for visibility
            p = plugin.plan()
            self.audit.record({"agent": "executor", "task_id": step["task_id"], "planned_actions": len(p)})
            if dry_run:
                results.append({"task": step["task_id"], "status": "planned", "plan": p})
                continue
            try:
                res = plugin.execute()
                results.append({"task": step["task_id"], "status": res.get("status", "ok"), "result": res})
            except Exception as e:
                self.audit.record({"agent": "executor", "task_id": step["task_id"], "error": str(e)})
                results.append({"task": step["task_id"], "status": "failed", "error": str(e)})
        return results
