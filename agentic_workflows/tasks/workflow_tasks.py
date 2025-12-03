"""Workflow execution tasks."""
from ..celery_app import celery_app
from ..core.orchestrator import Orchestrator
import structlog

logger = structlog.get_logger()

@celery_app.task(bind=True, max_retries=3)
def execute_workflow_task(self, workflow_id: str, spec_path: str):
    """Execute workflow as Celery task."""
    try:
        logger.info("executing_workflow", workflow_id=workflow_id)
        orchestrator = Orchestrator()
        result = orchestrator.run_spec(spec_path, dry_run=False)
        logger.info("workflow_completed", workflow_id=workflow_id)
        return result
    except Exception as exc:
        logger.error("workflow_failed", workflow_id=workflow_id, error=str(exc))
        raise self.retry(exc=exc, countdown=60)

@celery_app.task(bind=True, max_retries=3)
def execute_task_task(self, task_id: str, task_type: str, params: dict):
    """Execute single task as Celery task."""
    try:
        logger.info("executing_task", task_id=task_id, task_type=task_type)
        from ..core.agents import resolve_plugin
        
        plugin_class = resolve_plugin(task_type)
        plugin = plugin_class(params=params)
        result = plugin.execute()
        
        logger.info("task_completed", task_id=task_id)
        return result
    except Exception as exc:
        logger.error("task_failed", task_id=task_id, error=str(exc))
        raise self.retry(exc=exc, countdown=30)
