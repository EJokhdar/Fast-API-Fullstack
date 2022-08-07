import schema
import redis
import json
import ast
from sqlalchemy.orm import Session
from models import Todo
from redis import Redis
from fastapi import HTTPException, status, Body
from schema import TodoResponse
from celery_worker import expire_todo as expire_todo_task
from datetime import datetime, timedelta
from my_enums import Status
from dry_func import read_from_redis, read_task_or_404

CACHE_KEY_TEMPLATE = "task:{task_id}"


def get_all_tasks(db: Session):
    return db.query(Todo).all()


def get_task(db: Session, task_id: int, redis: Redis):
    cache_key = CACHE_KEY_TEMPLATE.format(task_id=task_id)
    response = read_from_redis(cache_key, redis)
    if response is not None:
        print("cache hit!!")
        return response

    print("cache miss!")

    task = read_task_or_404(task_id, db)

    redis.set(cache_key, TodoResponse.from_orm(task).json())

    return task


def create_task(db: Session, task: schema.TodoRequest):
    db_task = Todo(**task.dict())
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def delete_task(db: Session, task_id: int, redis: Redis):
    cache_key = CACHE_KEY_TEMPLATE.format(task_id=task_id)
    redis.delete(cache_key)

    task_delete = read_task_or_404(task_id, db)

    db.delete(task_delete)
    db.commit()
    return task_delete


def update_task(db: Session, task: schema.TodoRequest, task_id: int, redis: Redis):
    cache_key = CACHE_KEY_TEMPLATE.format(task_id=task_id)
    redis.delete(cache_key)

    task_update = read_task_or_404(task_id, db)

    task_update.task_name = task.task_name

    db.commit()
    return task_update


def toggle_task(db: Session, task_id: int, redis: Redis):
    cache_key = CACHE_KEY_TEMPLATE.format(task_id=task_id)
    redis.delete(cache_key)

    toggled_task = read_task_or_404(task_id, db)

    expire_time = toggled_task.expire_at.timestamp()
    current_time = datetime.now().timestamp()
    task_status = toggled_task.task_status

    if current_time > expire_time and task_status == "Task Expired":
        raise HTTPException(status.HTTP_408_REQUEST_TIMEOUT)

    toggled_task.checked = not toggled_task.checked

    if toggled_task.checked is True:
        toggled_task.task_status = Status.done.value
    else:
        toggled_task.task_status = Status.pending.value

    db.commit()
    return toggled_task


def expire_todo(db: Session, task: schema.TodoExpiryRequest, task_id: int, redis: Redis):

    task_timer = read_task_or_404(task_id, db)

    task_timer.expire_at = datetime.now() + timedelta(seconds=60)

    expire_todo_task.apply_async(
        args=[task_id], countdown=60)
    db.commit()
    return task_timer
