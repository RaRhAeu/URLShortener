from datetime import datetime

from celery.utils.log import get_task_logger

from urlshortener.database import db
from urlshortener.models import Url
from urlshortener.worker.celery import celery

logger = get_task_logger(__name__)


@celery.task
def increment_url_visits(short_url):
    url = Url.query(short_url=short_url).first()
    logger.info(f"Increasing visits on {url.id}")
    url.visits += 1
    db.session.commit()


@celery.task
def remove_expired_urls():
    logger.info("Deleting outdated urls")
    Url.query().filter(Url.expires_at <= datetime.utcnow()).delete()
    db.session.commit()


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, *args, **kwargs):
    sender.add_periodic_task(60.0,
                             remove_expired_urls.s(),
                             name="Remove expired urls task")
