from database import SessionLocal
from redis import Redis
from config import settings
from fastapi.security import OAuth2PasswordBearer


def get_token_scheme():
    return OAuth2PasswordBearer(tokenUrl="token")


def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_redis_client():
    return Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
