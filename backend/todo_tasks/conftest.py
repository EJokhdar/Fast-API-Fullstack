from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine, MetaData
from fastapi.testclient import TestClient
from database import Base
from main import app
from dependencies import get_db_session
from dependencies import get_redis_client
import pytest
from redis import Redis
from config import settings
from datetime import datetime
from my_enums import Status


engine = create_engine(
    settings.DB_URI, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture
def client():
    # def override_get_db_session():
    #     try:
    #         db = TestSessionLocal()
    #         yield db
    #     finally:
    #         db.close()
    # app.dependency_overrides[get_db_session] = override_get_db_session
    

    client = TestClient(app)

    yield client


@pytest.fixture
def redis():
    redis = Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
    return redis


@pytest.fixture(scope="function")
def create_delete_task(client):
    request = client.post(
        "/tasks",
        json={"task_name": "test code"}
    )

    yield request

    task = request.json()
    task_id = task["task_id"]

    response = client.delete(
        f"/tasks/{task_id}"
    )
    
