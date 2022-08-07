from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import create_engine
from config import settings

engine = create_engine(
    settings.DB_URI, echo=True)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine)

