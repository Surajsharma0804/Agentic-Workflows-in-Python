from .spec import load_spec
from .agents import PlannerAgent, ExecutorAgent
from .audit import AuditLog

class Orchestrator:
    def __init__(self, audit_path="audit.log"):
        self.audit = AuditLog(audit_path)
        self.planner = PlannerAgent(audit=self.audit)
        self.executor = ExecutorAgent(audit=self.audit)

    def run_spec(self, spec_path: str, dry_run: bool = True):
        spec = load_spec(spec_path)
        plan = self.planner.plan(spec)
        self.audit.record({"orchestrator": "starting_run", "spec": spec_path, "dry_run": dry_run})
        results = self.executor.execute_plan(plan, dry_run=dry_run)
        self.audit.record({"orchestrator": "run_complete", "spec": spec_path})
        return {"spec": spec.name, "plan": plan, "results": results}
