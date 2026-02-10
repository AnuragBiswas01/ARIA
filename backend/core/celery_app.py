"""
ARIA Celery Configuration
Sets up the Celery application for background tasks.
"""
import sys
from celery import Celery
from config.settings import settings

# Fix for Windows Celery support (if needed, though 'solo' pool or eventlet is better)
if sys.platform == "win32":
    import os
    os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

celery_app = Celery(
    "aria_worker",
    broker=settings.redis_url,
    backend=settings.redis_url,
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    # Windows compatibility: Use 'solo' or 'eventlet' pool when running the worker
    # worker_pool = 'solo'  <-- Set this via command line: celery -A core.celery_app worker --pool=solo
)

# Auto-discover tasks from other modules if needed
# celery_app.autodiscover_tasks(['services.some_service'])
