"""Celery application configuration."""
from celery import Celery
from .config import get_settings

settings = get_settings()

celery_app = Celery(
    "agentic_workflows",
    broker=settings.celery_broker_url,
    backend=settings.celery_result_backend,
    include=["agentic_workflows.tasks"]
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=settings.celery_task_track_started,
    task_time_limit=settings.celery_task_time_limit,
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
)
