import time
from celery import Celery
from config import settings
from sqlalchemy.orm import Session
from sqlalchemy import update, select
from schema import TodoExpiryRequest
from fastapi import Depends
from models import Todo
from dependencies import get_db_session
from database import SessionLocal
from dry_func import read_task_or_404
import datetime
from my_enums import Status


celery = Celery(__name__)
celery.conf.broker_url = f"{settings.REDIS_HOST}://{settings.REDIS_HOST}:{settings.REDIS_PORT}/{settings.REDIS_DB}"
celery.conf.result_backend = f"db+{settings.DB_URI}"


@celery.task(name="expire_todo", bind=True)
def expire_todo(self, task_id: int):
    session = SessionLocal()
    task_checked = read_task_or_404(task_id, session)

    if task_checked.checked is True:
        return "Task is already finished"
    else:
        stmt = (
            update(Todo).where(Todo.task_id == task_id).
            values(task_status=Status.expired.value)
        )
        session.execute(stmt)
        session.commit()
        session.close()
        return "Task Expired"
