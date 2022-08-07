import json
from redis import Redis
from sqlalchemy.orm import Session
from models import Todo, User
from fastapi import status, HTTPException


def read_from_redis(key: str, redis: Redis):
    byte_response = redis.get(key)
    if byte_response is None:
        return None
    else:
        return json.loads(byte_response.decode("UTF-8"))


def read_task_or_404(task_id: int, db: Session):
    task = db.query(Todo).filter(
        Todo.task_id == task_id).first()

    if task is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return task


def read_user_or_404(user_id: int, db: Session):
    user = db.query(User).filter(
        User.user_id == user_id). first()

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return user


def check_email_password(user_email, password, db: Session):
    user = db.query(User).filter(
        User.user_email == user_email and User.password == password).first()

    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND)

    return user
