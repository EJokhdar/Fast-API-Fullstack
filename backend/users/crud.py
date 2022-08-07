import redis
import json
from sqlalchemy.orm import Session
from models import User
from redis import Redis
from schema import UserLoginRequest, UserRegisterRequest, UserResponse, UserCredentials, UserChangePassword
from fastapi import HTTPException, status, Body
from dry_func import read_user_or_404, check_email_password

CACHE_USER_ID_TEMPLATE = "user:{user_id}"


def get_all_users(db: Session):
    return db.query(User).all()


def get_user(db: Session, user_id: int):
    task = read_user_or_404(user_id, db)
    return task


def create_user(db: Session, user: UserRegisterRequest):
    db_user = User(**user.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_credentials(db: Session, user: UserCredentials, user_id: int):
    user_cred = read_user_or_404(user_id, db)
    user_cred.user_name = user.user_name
    user_cred.user_email = user.user_email
    db.commit()
    return user_cred


def update_password(db: Session, user: UserChangePassword, user_id: int):
    user_password = read_user_or_404(user_id, db)
    user_password.user_password = user.password
    db.commit()
    return user_password


def delete_user(db: Session, user_id: int):
    user_delete = read_user_or_404(user_id, db)
    db.delete(user_delete)
    db.commit()
    return user_delete


def user_login(db: Session, user_email: str, password: str):
    user = check_email_password(user_email, password, db)
    hashed_password = user