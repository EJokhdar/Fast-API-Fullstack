from fastapi import FastAPI, status, HTTPException, Depends, Body
from fastapi.responses import JSONResponse
from database import SessionLocal, Base, engine
from typing import List
from schema import TodoResponse, TodoRequest, TodoExpiryRequest
from schema import UserResponse, UserRegisterRequest, UserLoginRequest, UserCredentials, UserChangePassword
from sqlalchemy.orm import Session
from redis import Redis
from dependencies import get_db_session
from dependencies import get_redis_client, get_token_scheme
import models
from todo_tasks import crud
from users import crud as user_crud
from celery_worker import expire_todo
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserRegisterRequest, db: Session = Depends(get_db_session)):
    return user_crud.create_user(db=db, user=user)


@app.get("/tasks", response_model=list[TodoResponse], status_code=status.HTTP_200_OK)
def get_all_tasks(db: Session = Depends(get_db_session)):
    return crud.get_all_tasks(db)


@app.post("/tasks", response_model=TodoResponse, status_code=status.HTTP_201_CREATED)
def create_tasks(task: TodoRequest, db: Session = Depends(get_db_session)):
    return crud.create_task(db=db, task=task)


@app.get("/tasks/{task_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def get_task(task_id: int, db: Session = Depends(get_db_session), redis: Redis = Depends(get_redis_client)):
    return crud.get_task(db=db, task_id=task_id, redis=redis)


@app.delete("/tasks/{task_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def delete_task(task_id: int, db: Session = Depends(get_db_session), redis: Redis = Depends(get_redis_client)):
    return crud.delete_task(db=db, task_id=task_id, redis=redis)


@app.put("/tasks/{task_id}", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def update_task(task_id: int, task: TodoRequest, db: Session = Depends(get_db_session), redis: Redis = Depends(get_redis_client)):
    return crud.update_task(db=db, task=task, task_id=task_id, redis=redis)


@app.post("/tasks/{task_id}/toggle", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def toggle_task(task_id: int, db: Session = Depends(get_db_session), redis: Redis = Depends(get_redis_client)):
    return crud.toggle_task(db=db, task_id=task_id, redis=redis)


@app.put("/tasks/{task_id}/expire", response_model=TodoResponse, status_code=status.HTTP_200_OK)
def expire_todo(task_id: int, task: TodoExpiryRequest, db: Session = Depends(get_db_session), redis: Redis = Depends(get_redis_client)):
    return crud.expire_todo(db=db, task=task, task_id=task_id, redis=redis)


@app.get("/users", response_model=list[UserResponse], status_code=status.HTTP_200_OK)
def get_all_users(db: Session = Depends(get_db_session)):
    user_crud.get_all_users(db)


@app.put("/users/{user_id}/changeCredentials", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_credentials(user_id: int, user: UserCredentials, db: Session = Depends(get_db_session)):
    return user_crud.update_credentials(db, user, user_id)


@app.delete("/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db_session)):
    return user_crud.delete_user(db, user_id)


@app.put("/users/{user_id}/changePassword", response_model=UserResponse, status_code=status.HTTP_200_OK)
def update_password(user_id: int, user: UserChangePassword, db: Session = Depends(get_db_session)):
    return user_crud.update_password(db, user, user_id)
