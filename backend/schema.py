from pydantic import BaseModel
from datetime import datetime


class TodoResponse(BaseModel):
    task_id: int
    task_name: str
    checked: bool
    task_status: str
    expire_at: datetime
    user_id: int

    class Config:
        orm_mode = True


class TodoRequest(BaseModel):
    task_name: str


class TodoExpiryRequest(BaseModel):
    expire_after: float


class UserResponse(BaseModel):
    user_id: int
    user_name: str
    user_email: str

    class Config:
        orm_mode = True


class UserRegisterRequest(BaseModel):
    user_name: str
    user_email: str
    password: str


class UserChangePassword(BaseModel):
    password: str


class UserCredentials(BaseModel):
    user_name: str
    user_email: str


class UserLoginRequest(BaseModel):
    user_email: str
    password: str
