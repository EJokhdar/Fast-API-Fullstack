from bcrypt import hashpw
from database import Base
from sqlalchemy import Column, String, Boolean, Integer, Float, DateTime, Enum, Text, ForeignKey
from datetime import datetime
from my_enums import Status


class Todo(Base):
    __tablename__ = "tasks"
    task_id = Column(Integer, primary_key=True)
    task_name = Column(String(255), nullable=False)
    checked = Column(Boolean, default=False)
    task_status = Column(String(255), default=Status.pending.value)
    expire_at = Column(DateTime, default=datetime.now(), nullable=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True)
    user_name = Column(String(255), nullable=False)
    user_email = Column(Text)
    password = Column(Text)

    def verify_password(self, password):
        pwhash = hashpw(password, self.password)
        return self.password == pwhash
