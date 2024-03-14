from celery import Celery
from celery.schedules import crontab

from src.services.organization import OrganizationService

celery = Celery(
    'tasks',
    broker_connection_retry_on_startup=True,
    broker='redis://localhost:6379'
)


@celery.task
async def update_tokens():
    organization_service = OrganizationService()
    print("update tokens")
    await organization_service.update_tokens()



celery.conf.beat_schedule = {
    'update-tokens-every-12-hours': {
        'task': 'tasks.update_tokens',
        'schedule': crontab(hour=0, minute=1),
    },
}