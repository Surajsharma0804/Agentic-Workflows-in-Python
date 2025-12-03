"""Prometheus metrics."""
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from functools import wraps
import time

# Workflow metrics
workflow_executions_total = Counter(
    'workflow_executions_total',
    'Total workflow executions',
    ['workflow_id', 'status']
)

workflow_duration_seconds = Histogram(
    'workflow_duration_seconds',
    'Workflow execution duration',
    ['workflow_id']
)

active_workflows = Gauge(
    'active_workflows',
    'Number of currently active workflows'
)

# Task metrics
task_executions_total = Counter(
    'task_executions_total',
    'Total task executions',
    ['task_type', 'status']
)

task_duration_seconds = Histogram(
    'task_duration_seconds',
    'Task execution duration',
    ['task_type']
)

# API metrics
api_requests_total = Counter(
    'api_requests_total',
    'Total API requests',
    ['method', 'endpoint', 'status']
)

api_request_duration_seconds = Histogram(
    'api_request_duration_seconds',
    'API request duration',
    ['method', 'endpoint']
)

def track_workflow_execution(workflow_id: str):
    """Decorator to track workflow execution metrics."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            active_workflows.inc()
            start_time = time.time()
            status = "success"
            
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                status = "failed"
                raise
            finally:
                duration = time.time() - start_time
                workflow_executions_total.labels(workflow_id=workflow_id, status=status).inc()
                workflow_duration_seconds.labels(workflow_id=workflow_id).observe(duration)
                active_workflows.dec()
        
        return wrapper
    return decorator

def get_metrics():
    """Get Prometheus metrics."""
    return generate_latest()
