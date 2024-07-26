from fastapi import FastAPI
from app.database import engine, Base
from app.endpoints import task

app = FastAPI()

app.include_router(task.router)

Base.metadata.create_all(bind=engine)