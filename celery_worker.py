from celery import Celery

from celery_tasks import process_blood_report  # 👈 Directly import your task

celery_app = Celery(
    "blood_tasks",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

