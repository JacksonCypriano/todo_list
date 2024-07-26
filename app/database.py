import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:admin@localhost:5432/tasks')

engine = create_engine(
    DATABASE_URL,
    connect_args={"options": "-c client_encoding=utf8"}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()