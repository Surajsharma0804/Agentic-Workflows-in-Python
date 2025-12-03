"""Celery worker entry point."""
from .celery_app import celery_app

def main():
    """Start Celery worker."""
    celery_app.worker_main([
        'worker',
        '--loglevel=info',
        '--concurrency=4',
        '--max-tasks-per-child=1000'
    ])

if __name__ == "__main__":
    main()
